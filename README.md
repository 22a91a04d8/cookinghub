# Cooking Hub - MongoDB with GridFS Integration

A Flask-based social media application for sharing cooking content with MongoDB database and GridFS file storage integration.

## Features

- User registration and authentication
- Image and video uploads (stored in MongoDB GridFS)
- Like and comment system
- Real-time chat between users
- Search functionality
- User profiles
- MongoDB database storage with GridFS for files

## Prerequisites

- Python 3.7 or higher
- MongoDB Community Server

## Installation

### 1. Install MongoDB

1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Install MongoDB on your system
3. Start MongoDB service

### 2. Setup Python Environment

```bash
# Navigate to the project directory
cd project1

# Install required packages
pip install -r requirements.txt
```

### 3. Run Setup Script

```bash
python setup_mongodb.py
```

This script will:
- Install required Python packages
- Test MongoDB connection
- Create sample data for testing

### 4. Run the Application

```bash
python app.py
```

Open your browser and go to: http://localhost:5000

## Database Structure

### Collections

1. **users** - User accounts and profiles
   - username (unique)
   - password
   - profile_pic_id (GridFS file ID)
   - profile_pic_filename
   - images (array of media items)
   - videos (array of media items)

2. **fs.files** - GridFS files collection (auto-created)
   - _id (file ID)
   - filename
   - content_type
   - length
   - uploadDate

3. **fs.chunks** - GridFS chunks collection (auto-created)
   - files_id (references fs.files)
   - n (chunk number)
   - data (binary data)

4. **likes** - Like relationships
   - file_id (GridFS file ID)
   - username

5. **comments** - Comments on media
   - file_id (GridFS file ID)
   - user
   - text
   - timestamp

6. **chats** - Chat messages
   - participants (array)
   - from
   - to
   - text
   - timestamp

## GridFS File Storage

This application uses MongoDB's GridFS for file storage instead of local file system:

### Benefits:
- ✅ Files stored directly in MongoDB
- ✅ No local file system dependencies
- ✅ Automatic file chunking for large files
- ✅ Built-in metadata storage
- ✅ Scalable across multiple servers
- ✅ No file path issues

### File Serving:
- Files are served via `/file/<file_id>` endpoint
- Automatic content-type detection
- Stream-based file delivery

## Configuration

The application uses the following default configuration:

- MongoDB URI: `mongodb://localhost:27017/`
- Database Name: `cooking_hub`
- GridFS: Automatically configured

You can modify these settings in `config.py`.

## Sample Users

The setup script creates these sample users for testing:

- Username: `chef_john`, Password: `password123`
- Username: `cooking_master`, Password: `password123`
- Username: `food_lover`, Password: `password123`

## File Structure

```
project1/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── database.py         # MongoDB and GridFS operations
├── requirements.txt    # Python dependencies
├── setup_mongodb.py    # Setup script
├── README.md          # This file
├── static/            # Static files (CSS, JS)
└── templates/         # HTML templates
```

## API Endpoints

- `GET /` - Login page
- `POST /login` - User login
- `GET/POST /signup` - User registration
- `GET /home` - Main feed
- `POST /like/<file_id>` - Like/unlike media
- `POST /comment/<file_id>` - Add comment
- `GET/POST /post` - Create new post
- `GET /profile` - User profile
- `GET/POST /charts` - Chat interface
- `POST /logout` - User logout
- `GET /file/<file_id>` - Serve files from GridFS

## Troubleshooting

### MongoDB Connection Issues

1. Ensure MongoDB service is running
2. Check if MongoDB is installed correctly
3. Verify the connection string in `config.py`

### GridFS Issues

1. Ensure MongoDB has sufficient storage space
2. Check MongoDB logs for GridFS errors
3. Verify file upload permissions

### Database Errors

1. Ensure MongoDB is running
2. Check database permissions
3. Verify collection names in `config.py`

## Security Notes

- Passwords are stored in plain text (consider hashing for production)
- File uploads should be validated for security
- Consider implementing rate limiting for production use
- GridFS provides built-in file validation

## Migration from Local Storage

If migrating from a previous version with local file storage:

1. Run the migration script: `python migrate_data.py`
2. The script will help transition to GridFS
3. Old local files can be safely removed after migration 