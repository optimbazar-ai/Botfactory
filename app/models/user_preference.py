"""User preference model for storing user-specific settings like language."""
from app import db
from datetime import datetime


class UserPreference(db.Model):
    """Model for storing user preferences (language, etc.)"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)
    telegram_user_id = db.Column(db.BigInteger, nullable=False)  # Telegram user ID
    language = db.Column(db.String(10), default='uz')  # uz, ru, en
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: one preference per user per bot
    __table_args__ = (
        db.UniqueConstraint('bot_id', 'telegram_user_id', name='unique_user_bot_preference'),
    )
    
    def __repr__(self):
        return f'<UserPreference bot={self.bot_id} user={self.telegram_user_id} lang={self.language}>'
