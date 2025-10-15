from datetime import datetime
from app import db


class Payment(db.Model):
    """Payment model for tracking subscription payments."""
    
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    amount = db.Column(db.Integer, nullable=False)  # Amount in UZS (sum)
    currency = db.Column(db.String(10), default='UZS', nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # payme, click, test
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, completed, failed, cancelled
    transaction_id = db.Column(db.String(100), nullable=True, index=True)
    subscription_type = db.Column(db.String(20), nullable=False)  # starter, basic, premium
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('payments', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.amount} {self.currency} via {self.payment_method}>'
    
    def get_amount_display(self):
        """Get formatted amount with currency."""
        return f"{self.amount:,} {self.currency}"
    
    def get_status_badge(self):
        """Get Bootstrap badge class for status."""
        badges = {
            'pending': 'warning',
            'completed': 'success',
            'failed': 'danger',
            'cancelled': 'secondary'
        }
        return badges.get(self.status, 'secondary')
