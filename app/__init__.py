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
    
    # Register blueprints
    try:
        from app.routes.main import main_bp
        app.register_blueprint(main_bp)
    except ImportError:
        print("⚠️ main route topilmadi")
    
    try:
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp)
    except ImportError:
        print("⚠️ auth route topilmadi")
    
    try:
        from app.routes.bot import bot_bp
        app.register_blueprint(bot_bp, url_prefix='/bots')
    except ImportError:
        print("⚠️ bot route topilmadi")
    
    try:
        from app.routes.telegram import telegram_bp
        app.register_blueprint(telegram_bp, url_prefix='/telegram')
    except ImportError:
        print("⚠️ telegram route topilmadi")
    
    try:
        from app.routes.kb import kb_bp
        app.register_blueprint(kb_bp, url_prefix='/kb')
    except ImportError:
        print("⚠️ kb route topilmadi")
    
    try:
        from app.routes.payment import payment_bp
        app.register_blueprint(payment_bp, url_prefix='/payment')
    except ImportError:
        print("⚠️ payment route topilmadi")
    
    try:
        from app.routes.bot_control import bot_control_bp
        app.register_blueprint(bot_control_bp)
    except ImportError:
        print("⚠️ bot_control route topilmadi")
    
    try:
        from app.routes.ai import ai_bp
        app.register_blueprint(ai_bp)
    except ImportError:
        print("⚠️ ai route topilmadi")
    
    try:
        from app.routes.admin import admin_bp
        app.register_blueprint(admin_bp)
    except ImportError:
        print("⚠️ admin route topilmadi")
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
