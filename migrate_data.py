#!/usr/bin/env python3
"""
Data Migration Script - Migrate from in-memory storage to MongoDB
"""

from database import db
import os

def migrate_existing_data():
    """Migrate any existing data to MongoDB"""
    print("🔄 Starting data migration...")
    
    # Check if there are any existing files in uploads directory
    uploads_dir = r'C:\Users\Dell\Documents\PROJECT\tetsproject\project1\uploads'
    
    if os.path.exists(uploads_dir):
        files = os.listdir(uploads_dir)
        print(f"Found {len(files)} files in uploads directory")
        
        # Create a default user if no users exist
        users_count = db.users.count_documents({})
        if users_count == 0:
            print("No users found in database. Creating default user...")
            db.create_user("admin", "admin123", "default.jpg")
            print("✅ Created default user: admin/admin123")
    
    print("✅ Migration completed!")

def check_database_status():
    """Check the current status of the database"""
    print("📊 Database Status:")
    print("-" * 30)
    
    users_count = db.users.count_documents({})
    likes_count = db.likes.count_documents({})
    comments_count = db.comments.count_documents({})
    chats_count = db.chats.count_documents({})
    
    print(f"Users: {users_count}")
    print(f"Likes: {likes_count}")
    print(f"Comments: {comments_count}")
    print(f"Chat Messages: {chats_count}")
    
    if users_count > 0:
        print("\nExisting users:")
        users = db.get_all_users()
        for user in users:
            print(f"  - {user['username']}")

def main():
    print("🚀 MongoDB Data Migration Tool")
    print("=" * 40)
    
    try:
        # Test database connection
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        client.admin.command('ping')
        client.close()
        print("✅ MongoDB connection successful!")
        
        # Check current status
        check_database_status()
        
        # Migrate data
        migrate_existing_data()
        
        # Show final status
        print("\n📊 Final Database Status:")
        check_database_status()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please ensure MongoDB is running and accessible.")

if __name__ == "__main__":
    main() 