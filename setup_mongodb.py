#!/usr/bin/env python3
"""
MongoDB Setup Script for Cooking Hub Application with GridFS
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def check_mongodb_connection():
    """Test MongoDB Atlas connection"""
    print("Testing MongoDB Atlas connection...")
    try:
        from database import db
        # Test the connection by trying to access the database
        db.db.list_collection_names()
        print("✅ MongoDB Atlas connection successful!")
        return True
    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {e}")
        print("\nPlease check your Atlas credentials in config.py")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    try:
        from database import db
        
        # Create sample users
        sample_users = [
            ("chef_john", "password123"),
            ("cooking_master", "password123"),
            ("food_lover", "password123")
        ]
        
        for username, password in sample_users:
            existing_user = db.get_user(username)
            if not existing_user:
                db.create_user(username, password)
                print(f"✅ Created user: {username}")
        
        print("✅ Sample data created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def main():
    print("🚀 Setting up MongoDB Atlas with GridFS for Cooking Hub Application")
    print("=" * 70)
    
    # Step 1: Install requirements
    if not install_requirements():
        return
    
    # Step 2: Check MongoDB Atlas connection
    if not check_mongodb_connection():
        return
    
    # Step 3: Create sample data
    if not create_sample_data():
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📁 Files will now be stored in MongoDB Atlas using GridFS")
    print("💾 No local file storage required!")
    print("☁️  Your data is safely stored in the cloud!")
    print("\nTo run the application:")
    print("python app.py")
    print("\nThen open your browser and go to: http://localhost:5000")

if __name__ == "__main__":
    main() 