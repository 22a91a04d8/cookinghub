from pymongo import MongoClient
from gridfs import GridFS
from config import Config
import os
import io
from bson import ObjectId

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB_NAME]
        
        # Collections
        self.users = self.db[Config.USERS_COLLECTION]
        self.chats = self.db[Config.CHATS_COLLECTION]
        self.likes = self.db[Config.LIKES_COLLECTION]
        self.comments = self.db[Config.COMMENTS_COLLECTION]
        
        # GridFS for file storage
        self.fs = GridFS(self.db)
        
        # Create indexes for better performance
        self.users.create_index("username", unique=True)
        self.likes.create_index([("filename", 1), ("username", 1)])
        self.comments.create_index("filename")
        self.chats.create_index([("participants", 1)])
    
    def store_file(self, file_data, filename, content_type=None):
        """Store a file in GridFS"""
        try:
            # Store file in GridFS
            file_id = self.fs.put(
                file_data,
                filename=filename,
                content_type=content_type
            )
            return str(file_id)
        except Exception as e:
            print(f"Error storing file: {e}")
            return None
    
    def get_file(self, file_id):
        """Get a file from GridFS"""
        try:
            # Convert string ID to ObjectId if needed
            if isinstance(file_id, str):
                file_id = ObjectId(file_id)
            return self.fs.get(file_id)
        except Exception as e:
            print(f"Error retrieving file: {e}")
            return None
    
    def delete_file(self, file_id):
        """Delete a file from GridFS"""
        try:
            self.fs.delete(file_id)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def create_user(self, username, password, profile_pic_data=None, profile_pic_filename='default.jpg'):
        """Create a new user"""
        profile_pic_id = None
        if profile_pic_data:
            profile_pic_id = self.store_file(profile_pic_data, profile_pic_filename)
        
        user_data = {
            'username': username,
            'password': password,
            'profile_pic_id': profile_pic_id,
            'profile_pic_filename': profile_pic_filename,
            'images': [],
            'videos': []
        }
        try:
            result = self.users.insert_one(user_data)
            return result.inserted_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user(self, username):
        """Get user by username"""
        return self.users.find_one({'username': username})
    
    def update_user_media(self, username, media_type, file_data, filename, description):
        """Add media (image/video) to user's collection"""
        # Store file in GridFS
        file_id = self.store_file(file_data, filename)
        if not file_id:
            return False
        
        media_item = {
            'file_id': file_id,
            'filename': filename,
            'description': description
        }
        
        if media_type == 'images':
            self.users.update_one(
                {'username': username},
                {'$push': {'images': media_item}}
            )
        elif media_type == 'videos':
            self.users.update_one(
                {'username': username},
                {'$push': {'videos': media_item}}
            )
        return True
    
    def get_all_users(self):
        """Get all users"""
        return list(self.users.find({}, {'password': 0}))  # Exclude password
    
    def get_all_media(self):
        """Get all media from all users"""
        all_media = []
        users = self.get_all_users()
        
        for user in users:
            username = user['username']
            
            # Add images
            for image in user.get('images', []):
                all_media.append({
                    'type': 'image',
                    'file_id': image['file_id'],
                    'filename': image['filename'],
                    'description': image['description'],
                    'username': username
                })
            
            # Add videos
            for video in user.get('videos', []):
                all_media.append({
                    'type': 'video',
                    'file_id': video['file_id'],
                    'filename': video['filename'],
                    'description': video['description'],
                    'username': username
                })
        
        return all_media
    
    def toggle_like(self, file_id, username):
        """Toggle like for a file"""
        existing_like = self.likes.find_one({
            'file_id': file_id,
            'username': username
        })
        
        if existing_like:
            # Unlike
            self.likes.delete_one({
                'file_id': file_id,
                'username': username
            })
            return False
        else:
            # Like
            self.likes.insert_one({
                'file_id': file_id,
                'username': username
            })
            return True
    
    def get_likes_count(self, file_id):
        """Get number of likes for a file"""
        return self.likes.count_documents({'file_id': file_id})
    
    def get_likes_for_file(self, file_id):
        """Get all usernames who liked a file"""
        likes = self.likes.find({'file_id': file_id})
        return [like['username'] for like in likes]
    
    def add_comment(self, file_id, username, comment_text):
        """Add a comment to a file"""
        comment_data = {
            'file_id': file_id,
            'user': username,
            'text': comment_text,
            'timestamp': os.urandom(8).hex()  # Simple timestamp
        }
        return self.comments.insert_one(comment_data)
    
    def get_comments_for_file(self, file_id):
        """Get all comments for a file"""
        comments = self.comments.find({'file_id': file_id}).sort('timestamp', 1)
        return list(comments)
    
    def add_chat_message(self, sender, receiver, message):
        """Add a chat message"""
        participants = sorted([sender, receiver])
        chat_data = {
            'participants': participants,
            'from': sender,
            'to': receiver,
            'text': message,
            'timestamp': os.urandom(8).hex()
        }
        return self.chats.insert_one(chat_data)
    
    def get_chat_messages(self, user1, user2):
        """Get chat messages between two users"""
        participants = sorted([user1, user2])
        messages = self.chats.find({'participants': participants}).sort('timestamp', 1)
        return list(messages)
    
    def search_users(self, search_term):
        """Search users by username"""
        regex_pattern = {'$regex': search_term, '$options': 'i'}
        users = self.users.find({'username': regex_pattern}, {'password': 0})
        return list(users)
    
    def search_media(self, search_term):
        """Search media by description"""
        all_media = self.get_all_media()
        if not search_term:
            return all_media
        
        search_term = search_term.lower()
        filtered_media = []
        
        for media in all_media:
            if search_term in media['description'].lower():
                filtered_media.append(media)
        
        return filtered_media

# Global database instance
db = Database() 