"""
Migration script to add user_preferences table.
Run this inside Flask shell or when app starts.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

def migrate():
    app = create_app()
    
    with app.app_context():
        print("Creating user_preferences table...")
        # Import model to register it
        from app.models.user_preference import UserPreference
        db.create_all()
        print("✅ User preferences table created successfully!")

if __name__ == '__main__':
    migrate()
