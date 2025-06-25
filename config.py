import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv is not installed, we'll use environment variables directly
    pass

class Config:
    SECRET_KEY = 'd3aF9Z@w!v6xT#kYpL2zR$eM0bNhQ8Vc'
    UPLOAD_FOLDER = r'C:\Users\Dell\Documents\PROJECT\tetsproject\project1\uploads'
    
    # MongoDB Atlas Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://22a91a04d1:lokeshlucky333@cluster0.gesokh4.mongodb.net/')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'cooking_hub')
    
    # Collection names
    USERS_COLLECTION = 'users'
    CHATS_COLLECTION = 'chats'
    LIKES_COLLECTION = 'likes'
    COMMENTS_COLLECTION = 'comments' 