"""
Admin user'ni to'g'ri parol hash bilan qayta yaratish
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User

def fix_admin_user():
    app = create_app()
    
    with app.app_context():
        # Delete existing admin user
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            print("🗑️ Deleted existing admin user with invalid hash")
        
        # Create new admin user with correct bcrypt hash
        admin_user = User(
            username='admin',
            email='admin@botfactory.com',
            is_admin=True,
            subscription_type='premium'
        )
        admin_user.set_password('123456')  # This uses bcrypt correctly
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Admin user recreated with correct bcrypt hash!")
        print("   Username: admin")
        print("   Password: 123456")
        print("   Email: admin@botfactory.com")
        print("   Type: Premium Admin")

if __name__ == '__main__':
    fix_admin_user()
