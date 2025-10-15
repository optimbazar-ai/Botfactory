"""
Main routes - asosiy sahifalar
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app.models.bot import BotModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Asosiy sahifa"""
    if current_user.is_authenticated:
        # Foydalanuvchi tizimga kirgan bo'lsa, botlar sahifasiga yo'naltirish
        return redirect(url_for('bot.list_bots'))
    
    # Mehmon foydalanuvchilar uchun landing page
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard sahifasi"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Foydalanuvchi botlari
    user_bots = BotModel.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html', bots=user_bots)

@main_bp.route('/about')
def about():
    """Loyiha haqida"""
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    """Aloqa sahifasi"""
    return render_template('contact.html')
