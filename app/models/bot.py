from datetime import datetime
from app import db


class Bot(db.Model):
    """Bot model for managing user's bots."""
    
    __tablename__ = 'bots'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    language = db.Column(db.String(10), nullable=False, default='uz')
    platform = db.Column(db.String(20), nullable=False, default='telegram')
    system_prompt = db.Column(db.Text, nullable=True)
    
    # Multiple Telegram tokens support
    telegram_token_1 = db.Column(db.String(100), nullable=True)
    telegram_token_2 = db.Column(db.String(100), nullable=True)
    telegram_token_3 = db.Column(db.String(100), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('bots', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Bot {self.name} ({self.platform})>'
    
    def get_telegram_tokens(self):
        """Get all non-empty telegram tokens."""
        tokens = []
        if self.telegram_token_1:
            tokens.append(self.telegram_token_1)
        if self.telegram_token_2:
            tokens.append(self.telegram_token_2)
        if self.telegram_token_3:
            tokens.append(self.telegram_token_3)
        # Fallback to old telegram_token field for backward compatibility
        if not tokens and hasattr(self, 'telegram_token') and self.telegram_token:
            tokens.append(self.telegram_token)
        return tokens
