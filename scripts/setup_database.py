"""
Database setup script for AI Website Builder
This script initializes the Firebase Firestore database with necessary collections and indexes.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import json

def setup_database():
    """Initialize Firebase and create necessary collections"""
    
    # Initialize Firebase Admin SDK
    try:
        # Use your Firebase service account key
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("✅ Firebase initialized successfully")
        
        # Create collections with sample documents to establish structure
        
        # Users collection
        users_ref = db.collection('users')
        sample_user = {
            'name': 'Sample User',
            'email': 'sample@example.com',
            'createdAt': firestore.SERVER_TIMESTAMP,
            'settings': {
                'emailNotifications': True,
                'darkMode': False
            }
        }
        users_ref.document('sample_user_id').set(sample_user)
        print("✅ Users collection created")
        
        # Projects collection
        projects_ref = db.collection('projects')
        sample_project = {
            'id': 'sample_project_id',
            'user_id': 'sample_user_id',
            'title': 'Sample Website',
            'prompt': 'Create a modern portfolio website',
            'code': '<!DOCTYPE html><html><head><title>Sample</title></head><body><h1>Sample Website</h1></body></html>',
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'tags': ['portfolio', 'modern'],
            'is_public': False
        }
        projects_ref.document('sample_project_id').set(sample_project)
        print("✅ Projects collection created")
        
        # Analytics collection for tracking usage
        analytics_ref = db.collection('analytics')
        sample_analytics = {
            'user_id': 'sample_user_id',
            'action': 'website_generated',
            'timestamp': firestore.SERVER_TIMESTAMP,
            'metadata': {
                'prompt_length': 25,
                'generation_time': 12.5,
                'model_used': 'mixtral-8x7b-32768'
            }
        }
        analytics_ref.add(sample_analytics)
        print("✅ Analytics collection created")
        
        print("\n🎉 Database setup completed successfully!")
        print("You can now delete the sample documents if needed.")
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    setup_database()
