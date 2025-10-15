from datetime import datetime
from app import db


class KnowledgeBase(db.Model):
    """Knowledge Base model for storing bot context documents."""
    
    __tablename__ = 'knowledge_bases'
    
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # txt, docx
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to Bot
    bot = db.relationship('Bot', backref=db.backref('knowledge_bases', lazy='dynamic', cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<KnowledgeBase {self.filename} for Bot {self.bot_id}>'
    
    def get_size_display(self):
        """Get human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} GB"
