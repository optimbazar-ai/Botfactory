from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # User loader for Flask-Login
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints - faqat asosiy route'lar
    print("🔄 Route'larni yuklash...")
    
    # Main route
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    print("✅ Main route yuklandi")
    
    # Auth route  
    try:
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp)
        print("✅ Auth route yuklandi")
    except Exception as e:
        print(f"❌ Auth route xatolik: {e}")
    
    # Bot route
    try:
        from app.routes.bot import bot_bp
        app.register_blueprint(bot_bp, url_prefix='/bots')
        print("✅ Bot route yuklandi")
    except Exception as e:
        print(f"❌ Bot route xatolik: {e}")
    
    # Telegram route
    try:
        from app.routes.telegram import telegram_bp
        app.register_blueprint(telegram_bp, url_prefix='/telegram')
        print("✅ Telegram route yuklandi")
    except Exception as e:
        print(f"❌ Telegram route xatolik: {e}")
    
    print("🎉 Route'lar yuklandi!")
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
