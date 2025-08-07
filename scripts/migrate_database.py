"""
Database migration script for AI Website Builder
This script handles database schema updates and data migrations.
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json

def migrate_database():
    """Run database migrations"""
    
    try:
        # Initialize Firebase if not already done
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-credentials.json')
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("🔄 Starting database migration...")
        
        # Migration 1: Add missing fields to existing projects
        migrate_projects_add_fields(db)
        
        # Migration 2: Update user settings structure
        migrate_user_settings(db)
        
        # Migration 3: Add indexes for better query performance
        create_indexes(db)
        
        print("✅ All migrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False
    
    return True

def migrate_projects_add_fields(db):
    """Add missing fields to existing projects"""
    print("🔄 Migrating projects collection...")
    
    projects_ref = db.collection('projects')
    projects = projects_ref.stream()
    
    batch = db.batch()
    count = 0
    
    for project in projects:
        project_data = project.to_dict()
        project_ref = projects_ref.document(project.id)
        
        updates = {}
        
        # Add tags field if missing
        if 'tags' not in project_data:
            updates['tags'] = []
        
        # Add is_public field if missing
        if 'is_public' not in project_data:
            updates['is_public'] = False
        
        # Add updated_at field if missing
        if 'updated_at' not in project_data:
            updates['updated_at'] = project_data.get('created_at', firestore.SERVER_TIMESTAMP)
        
        # Add version field for tracking
        if 'version' not in project_data:
            updates['version'] = 1
        
        if updates:
            batch.update(project_ref, updates)
            count += 1
    
    if count > 0:
        batch.commit()
        print(f"✅ Updated {count} projects")
    else:
        print("✅ No projects needed updating")

def migrate_user_settings(db):
    """Update user settings structure"""
    print("🔄 Migrating user settings...")
    
    users_ref = db.collection('users')
    users = users_ref.stream()
    
    batch = db.batch()
    count = 0
    
    for user in users:
        user_data = user.to_dict()
        user_ref = users_ref.document(user.id)
        
        updates = {}
        
        # Add settings object if missing
        if 'settings' not in user_data:
            updates['settings'] = {
                'emailNotifications': True,
                'darkMode': False,
                'autoSave': True,
                'defaultPrivacy': 'private'
            }
        else:
            # Update existing settings with new fields
            settings = user_data['settings']
            if 'autoSave' not in settings:
                settings['autoSave'] = True
            if 'defaultPrivacy' not in settings:
                settings['defaultPrivacy'] = 'private'
            updates['settings'] = settings
        
        # Add profile completion status
        if 'profileComplete' not in user_data:
            updates['profileComplete'] = bool(user_data.get('name'))
        
        if updates:
            batch.update(user_ref, updates)
            count += 1
    
    if count > 0:
        batch.commit()
        print(f"✅ Updated {count} users")
    else:
        print("✅ No users needed updating")

def create_indexes(db):
    """Create database indexes for better performance"""
    print("🔄 Creating database indexes...")
    
    # Note: Firestore indexes are typically created through the Firebase Console
    # or using the Firebase CLI. This function documents the required indexes.
    
    required_indexes = [
        {
            'collection': 'projects',
            'fields': [
                {'field': 'user_id', 'order': 'ASCENDING'},
                {'field': 'created_at', 'order': 'DESCENDING'}
            ]
        },
        {
            'collection': 'projects',
            'fields': [
                {'field': 'user_id', 'order': 'ASCENDING'},
                {'field': 'is_public', 'order': 'ASCENDING'},
                {'field': 'created_at', 'order': 'DESCENDING'}
            ]
        },
        {
            'collection': 'analytics',
            'fields': [
                {'field': 'user_id', 'order': 'ASCENDING'},
                {'field': 'timestamp', 'order': 'DESCENDING'}
            ]
        }
    ]
    
    print("📋 Required indexes:")
    for index in required_indexes:
        print(f"  Collection: {index['collection']}")
        for field in index['fields']:
            print(f"    - {field['field']} ({field['order']})")
        print()
    
    print("ℹ️  Please create these indexes in the Firebase Console or using Firebase CLI")
    print("✅ Index documentation completed")

if __name__ == "__main__":
    migrate_database()
