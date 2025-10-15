from datetime import datetime
from flask_login import UserMixin
from app import db
import bcrypt


class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)  # Phone number (optional)
    password_hash = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(10), default='uz', nullable=False)
    subscription_type = db.Column(db.String(20), default='free', nullable=False)
    subscription_end_date = db.Column(db.DateTime, nullable=True)  # When subscription expires
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def set_password(self, password):
        """Hash and set the user's password using bcrypt."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        """Verify a password against the stored hash."""
        password_bytes = password.encode('utf-8')
        password_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)
    
    def is_subscription_active(self):
        """Check if user's subscription is still active."""
        if self.subscription_type == 'free':
            return True
        if not self.subscription_end_date:
            return False
        return self.subscription_end_date > datetime.utcnow()
    
    def get_subscription_status(self):
        """Get subscription status display."""
        if self.subscription_type == 'free':
            return 'Free Plan'
        if self.is_subscription_active():
            days_left = (self.subscription_end_date - datetime.utcnow()).days
            return f'{self.subscription_type.capitalize()} ({days_left} days left)'
        return f'{self.subscription_type.capitalize()} (Expired)'
    
    def __repr__(self):
        return f'<User {self.username}>'
