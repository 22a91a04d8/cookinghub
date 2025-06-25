#!/usr/bin/env python3
"""
Database Test Script - Test all database operations
"""

from database import db
import io

def test_user_operations():
    """Test user creation and retrieval"""
    print("🧪 Testing User Operations...")
    
    # Test user creation
    user_id = db.create_user("test_user_123", "test_password")
    print(f"✅ User created with ID: {user_id}")
    
    # Test user retrieval
    user = db.get_user("test_user_123")
    if user:
        print(f"✅ User retrieved: {user['username']}")
    else:
        print("❌ User retrieval failed")
    
    # Test duplicate user creation
    duplicate_id = db.create_user("test_user_123", "test_password")
    if duplicate_id is None:
        print("✅ Duplicate user properly rejected")
    else:
        print("❌ Duplicate user was created (should be rejected)")

def test_file_operations():
    """Test GridFS file operations"""
    print("\n🧪 Testing File Operations...")
    
    # Test file storage
    test_content = b"This is a test file content for GridFS"
    file_data = io.BytesIO(test_content)
    file_id = db.store_file(file_data, "test_file.txt")
    print(f"✅ File stored with ID: {file_id}")
    
    # Test file retrieval
    retrieved_file = db.get_file(file_id)
    if retrieved_file:
        content = retrieved_file.read()
        if content == test_content:
            print("✅ File retrieved successfully")
        else:
            print("❌ File content mismatch")
    else:
        print("❌ File retrieval failed")

def test_media_operations():
    """Test media upload operations"""
    print("\n🧪 Testing Media Operations...")
    
    # Create a test user first
    db.create_user("media_test_user", "password123")
    
    # Test image upload
    image_content = b"fake image data"
    image_data = io.BytesIO(image_content)
    success = db.update_user_media("media_test_user", "images", image_data, "test_image.jpg", "Test image description")
    
    if success:
        print("✅ Image upload successful")
    else:
        print("❌ Image upload failed")
    
    # Test video upload
    video_content = b"fake video data"
    video_data = io.BytesIO(video_content)
    success = db.update_user_media("media_test_user", "videos", video_data, "test_video.mp4", "Test video description")
    
    if success:
        print("✅ Video upload successful")
    else:
        print("❌ Video upload failed")

def test_like_comment_operations():
    """Test like and comment operations"""
    print("\n🧪 Testing Like/Comment Operations...")
    
    # Create a test file first
    test_content = b"test content"
    file_data = io.BytesIO(test_content)
    file_id = db.store_file(file_data, "test_like_file.txt")
    
    # Test like operations
    db.toggle_like(file_id, "test_user_123")
    likes = db.get_likes_for_file(file_id)
    print(f"✅ Like count: {len(likes)}")
    
    # Test comment operations
    db.add_comment(file_id, "test_user_123", "This is a test comment")
    comments = db.get_comments_for_file(file_id)
    print(f"✅ Comment count: {len(comments)}")

def test_chat_operations():
    """Test chat operations"""
    print("\n🧪 Testing Chat Operations...")
    
    # Test chat message
    db.add_chat_message("user1", "user2", "Hello from user1!")
    messages = db.get_chat_messages("user1", "user2")
    print(f"✅ Chat messages: {len(messages)}")

def main():
    print("🚀 Database Test Suite")
    print("=" * 50)
    
    try:
        test_user_operations()
        test_file_operations()
        test_media_operations()
        test_like_comment_operations()
        test_chat_operations()
        
        print("\n🎉 All tests completed!")
        print("✅ Database operations are working correctly")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Please check your MongoDB Atlas connection and credentials")

if __name__ == "__main__":
    main() 