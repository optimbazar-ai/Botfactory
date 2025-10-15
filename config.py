import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class."""
    
    # Get SECRET_KEY from environment, raise error if missing
    SECRET_KEY = os.environ.get('SESSION_SECRET')
    if not SECRET_KEY:
        raise ValueError("SESSION_SECRET environment variable is required")
    
    # Google Gemini API Key (required for AI features)
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    # Database configuration
    # Use PostgreSQL if DATABASE_URL is set, otherwise SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///botfactory.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-WTF CSRF protection
    WTF_CSRF_ENABLED = True
