"""
Test foydalanuvchi yaratish scripti
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User

def create_test_user():
    app = create_app()
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            print("✅ Test user 'admin' already exists!")
            print(f"   Username: admin")
            print(f"   Email: {existing_user.email}")
            return
        
        # Create test user
        test_user = User(
            username='admin',
            email='admin@botfactory.com',
            is_admin=True,
            subscription_type='premium'
        )
        test_user.set_password('123456')
        
        db.session.add(test_user)
        db.session.commit()
        
        print("✅ Test user created successfully!")
        print("   Username: admin")
        print("   Password: 123456")
        print("   Email: admin@botfactory.com")
        print("   Type: Premium Admin")

if __name__ == '__main__':
    create_test_user()
