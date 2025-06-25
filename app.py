from flask import *
import os
from werkzeug.utils import secure_filename
from config import Config
from database import db
import io

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    user = db.get_user(username)
    if user and user['password'] == password:
        session['username'] = username
        return redirect(url_for('home'))
    return "Invalid username or password"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if user already exists
        existing_user = db.get_user(username)
        if existing_user:
            return "User already exists."
        
        if password != confirm_password:
            return "Passwords do not match."

        profile_pic = request.files.get('profile_pic')
        profile_pic_data = None
        profile_pic_filename = 'default.jpg'
        
        if profile_pic and profile_pic.filename:
            profile_pic_filename = secure_filename(profile_pic.filename)
            profile_pic_data = profile_pic.read()

        # Create user in database
        result = db.create_user(username, password, profile_pic_data, profile_pic_filename)
        if result:
            return redirect(url_for('login'))
        else:
            return "Error creating user. Please try again."
    
    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    current_user = session['username']
    search = request.args.get('search', '').lower()
    
    # Get all media and users
    all_media = db.get_all_media()
    all_users = db.get_all_users()
    
    # Filter media and users based on search
    matched_users = []
    filtered_media = []
    
    if search:
        # Search users
        matched_users = [user['username'] for user in db.search_users(search)]
        
        # Search media
        filtered_media = db.search_media(search)
    else:
        filtered_media = all_media

    # Convert users list to dict for template compatibility
    users_dict = {user['username']: user for user in all_users}
    
    # Get likes and comments for all media
    likes_data = {}
    comments_data = {}
    
    for media in filtered_media:
        file_id = media['file_id']
        likes_data[file_id] = db.get_likes_for_file(file_id)
        comments_data[file_id] = db.get_comments_for_file(file_id)

    return render_template('home.html',
                           username=current_user,
                           all_media=filtered_media,
                           matched_users=matched_users,
                           users=users_dict,
                           likes=likes_data,
                           comments=comments_data)

@app.route('/like/<file_id>', methods=['POST'])
def like(file_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = session['username']
    db.toggle_like(file_id, user)
    return redirect(url_for('home'))

@app.route('/comment/<file_id>', methods=['POST'])
def comment(file_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = session['username']
    comment_text = request.form.get('comment')
    if comment_text:
        db.add_comment(file_id, user, comment_text)
    return redirect(url_for('home'))

@app.route('/post', methods=['GET', 'POST'])
def post():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files.get('media')
        description = request.form.get('description')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_data = file.read()
            media_type = 'videos' if filename.lower().endswith(('.mp4', '.avi', '.mov')) else 'images'
            success = db.update_user_media(session['username'], media_type, file_data, filename, description)
            if not success:
                return "Error uploading file. Please try again."
        return redirect(url_for('profile'))
    return render_template('post.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user = db.get_user(username)
    
    if not user:
        return redirect(url_for('login'))
    
    profile_pic_filename = user.get('profile_pic_filename', 'default.jpg')
    profile_pic_id = user.get('profile_pic_id')
    
    return render_template('profile.html',
                           username=username,
                           profile_pic_filename=profile_pic_filename,
                           profile_pic_id=profile_pic_id,
                           user_images=user.get('images', []),
                           user_videos=user.get('videos', []))

@app.route('/charts', methods=['GET', 'POST'])
def charts():
    if 'username' not in session:
        return redirect(url_for('login'))

    sender = session['username']
    receiver = request.args.get('receiver')
    messages = []
    receiver_pic_filename = None
    receiver_pic_id = None

    if receiver:
        # Get chat messages
        messages = db.get_chat_messages(sender, receiver)
        
        # Get receiver's profile pic
        receiver_user = db.get_user(receiver)
        if receiver_user:
            receiver_pic_filename = receiver_user.get('profile_pic_filename', 'default.jpg')
            receiver_pic_id = receiver_user.get('profile_pic_id')

        if request.method == 'POST':
            text = request.form['message']
            db.add_chat_message(sender, receiver, text)
            return redirect(url_for('charts', receiver=receiver))

    # Get all users for the user list
    all_users = db.get_all_users()
    users_dict = {user['username']: user for user in all_users}

    return render_template('charts.html',
                           users=users_dict,
                           current_user=sender,
                           receiver=receiver,
                           receiver_pic_filename=receiver_pic_filename,
                           receiver_pic_id=receiver_pic_id,
                           messages=messages)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/file/<file_id>')
def serve_file(file_id):
    """Serve files from GridFS"""
    try:
        file_obj = db.get_file(file_id)
        if file_obj:
            return send_file(
                io.BytesIO(file_obj.read()),
                mimetype=file_obj.content_type or 'application/octet-stream'
            )
        else:
            return "File not found", 404
    except Exception as e:
        return f"Error serving file: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
