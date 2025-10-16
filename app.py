"""
BotFactory - Telegram Bot Yaratish Platformasi
"""
import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Environment variables yuklash
load_dotenv()

# Bot manager import (keyinroq ishga tushiramiz)
from services.bot_manager import BotManager
bot_manager = None

# Flask app yaratish
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Database URI (Render.com postgres:// ni postgresql:// ga o'zgartirish)
database_url = os.getenv('DATABASE_URL', 'sqlite:///botfactory_new.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database va Login Manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Iltimos, avval tizimga kiring"


# ========== MODELS ==========

class User(UserMixin, db.Model):
    """Foydalanuvchi modeli"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Subscription
    is_premium = db.Column(db.Boolean, default=False)
    trial_start = db.Column(db.DateTime, default=datetime.utcnow)
    trial_end = db.Column(db.DateTime)
    messages_used = db.Column(db.Integer, default=0)
    
    # Admin
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bots = db.relationship('Bot', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 15 kunlik test muddati
        if not self.trial_end:
            self.trial_end = datetime.utcnow() + timedelta(days=15)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_trial_active(self):
        """Test muddati faolmi?"""
        return datetime.utcnow() <= self.trial_end
    
    def can_send_message(self):
        """Xabar yuborish imkoniyati"""
        if self.is_premium:
            return True
        if self.is_trial_active() and self.messages_used < 500:
            return True
        return False
    
    def get_days_left(self):
        """Qolgan kunlar"""
        if self.is_premium:
            return "Cheksiz"
        delta = self.trial_end - datetime.utcnow()
        return max(0, delta.days)


class Bot(db.Model):
    """Bot modeli"""
    __tablename__ = 'bots'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    telegram_token = db.Column(db.String(100))
    telegram_username = db.Column(db.String(50))
    language = db.Column(db.String(10), default='uz')
    system_prompt = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=False)
    admin_chat_id = db.Column(db.String(50))
    notification_channel = db.Column(db.String(100))
    notifications_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Statistics
    total_messages = db.Column(db.Integer, default=0)
    today_messages = db.Column(db.Integer, default=0)
    last_message_date = db.Column(db.Date)
    
    # Relationships
    messages = db.relationship('Message', backref='bot', lazy='dynamic', cascade='all, delete-orphan')


class Message(db.Model):
    """Xabarlar modeli"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)
    telegram_user_id = db.Column(db.BigInteger)
    telegram_username = db.Column(db.String(50))
    message_text = db.Column(db.Text)
    is_from_user = db.Column(db.Boolean, default=True)
    is_spam = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ========== LOGIN MANAGER ==========

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ========== ROUTES ==========

@app.route('/health')
def health_check():
    """Health check endpoint - Render.com va monitoring uchun"""
    try:
        # Database connection tekshirish
        db.session.execute(db.text('SELECT 1'))
        return {
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, 500

@app.route('/')
def index():
    """Bosh sahifa"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Ro'yxatdan o'tish"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        # Tekshirish
        if User.query.filter_by(username=username).first():
            flash('Bu username band!', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Bu email band!', 'danger')
            return redirect(url_for('register'))
        
        # Yangi foydalanuvchi
        user = User(
            username=username,
            email=email,
            phone=phone
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Ro\'yxatdan muvaffaqiyatli o\'tdingiz! 15 kunlik test muddati boshlandi.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Tizimga kirish"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Sizning akkountingiz bloklangan!', 'danger')
                return redirect(url_for('login'))
            
            login_user(user, remember=True)
            flash(f'Xush kelibsiz, {user.username}!', 'success')
            
            # Admin bo'lsa admin panelga
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            
            return redirect(url_for('dashboard'))
        
        flash('Username yoki parol xato!', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Chiqish"""
    logout_user()
    flash('Tizimdan chiqdingiz!', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Foydalanuvchi dashboard"""
    user_bots = current_user.bots.all()
    
    # Statistika
    stats = {
        'total_bots': len(user_bots),
        'active_bots': len([b for b in user_bots if b.is_active]),
        'messages_used': current_user.messages_used,
        'messages_limit': 500 if not current_user.is_premium else 'Cheksiz',
        'days_left': current_user.get_days_left(),
        'is_premium': current_user.is_premium
    }
    
    return render_template('dashboard.html', bots=user_bots, stats=stats)


@app.route('/bot/create', methods=['GET', 'POST'])
@login_required
def create_bot():
    """Bot yaratish"""
    # Cheklovlar
    bot_count = current_user.bots.count()
    max_bots = 3 if current_user.is_premium else 1
    
    if bot_count >= max_bots:
        flash(f'Siz maksimal {max_bots} ta bot yaratishingiz mumkin!', 'warning')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        telegram_token = request.form.get('telegram_token')
        language = request.form.get('language', 'uz')
        system_prompt = request.form.get('system_prompt')
        
        # Admin chat va bildirishnoma sozlamalari
        admin_chat_id = request.form.get('admin_chat_id')
        notification_channel = request.form.get('notification_channel')
        notifications_enabled = request.form.get('notifications_enabled') == 'on'
        
        # Bot yaratish
        bot = Bot(
            user_id=current_user.id,
            name=name,
            description=description,
            telegram_token=telegram_token,
            language=language,
            system_prompt=system_prompt,
            admin_chat_id=admin_chat_id,
            notification_channel=notification_channel,
            notifications_enabled=notifications_enabled
        )
        
        # Telegram username olish (agar token to'g'ri bo'lsa)
        if telegram_token:
            try:
                from telegram import Bot as TelegramBot
                tg_bot = TelegramBot(token=telegram_token)
                bot_info = tg_bot.get_me()
                bot.telegram_username = bot_info.username
            except:
                pass
        
        db.session.add(bot)
        db.session.commit()
        
        # Agar token berilgan bo'lsa, botni avtomatik ishga tushirish
        if telegram_token and bot_manager:
            try:
                result = bot_manager.start_bot(bot)
                if result['success']:
                    flash('Bot muvaffaqiyatli yaratildi va ishga tushirildi! ✅', 'success')
                else:
                    flash(f'Bot yaratildi, lekin ishga tushmadi: {result["message"]}', 'warning')
            except Exception as e:
                flash(f'Bot yaratildi, lekin xatolik: {str(e)}', 'warning')
        else:
            flash('Bot yaratildi! Endi uni ishga tushirishingiz kerak.', 'success')
        
        return redirect(url_for('view_bot', bot_id=bot.id))
    
    return render_template('create_bot.html')


@app.route('/bot/<int:bot_id>')
@login_required
def view_bot(bot_id):
    """Bot ko'rish"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi ko'ra oladi
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botni ko\'rish huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Statistika
    today = datetime.utcnow().date()
    if bot.last_message_date != today:
        bot.today_messages = 0
        bot.last_message_date = today
        db.session.commit()
    
    return render_template('view_bot.html', bot=bot)


@app.route('/bot/<int:bot_id>/edit')
@login_required
def edit_bot(bot_id):
    """Bot tahrirlash sahifasi"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi tahrirlashi mumkin
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botni tahrirlash huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_bot_modern.html', bot=bot)


@app.route('/bot/<int:bot_id>/update', methods=['POST'])
@login_required
def update_bot(bot_id):
    """Bot yangilash"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi tahrirlashi mumkin
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botni tahrirlash huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Ma'lumotlarni yangilash
    bot.name = request.form.get('name')
    bot.description = request.form.get('description')
    bot.language = request.form.get('language', 'uz')
    bot.system_prompt = request.form.get('system_prompt')
    
    # Yangi maydonlar
    bot.admin_chat_id = request.form.get('admin_chat_id')
    bot.notification_channel = request.form.get('notification_channel')
    bot.notifications_enabled = request.form.get('notifications_enabled') == 'on'
    
    # Telegram token yangilash
    new_token = request.form.get('telegram_token')
    if new_token and new_token != bot.telegram_token:
        bot.telegram_token = new_token
        # Token yangilangan bo'lsa, username ni ham yangilash kerak
        try:
            import requests
            response = requests.get(f'https://api.telegram.org/bot{new_token}/getMe')
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    bot.telegram_username = bot_info['result']['username']
        except:
            pass
    
    db.session.commit()
    flash('Bot muvaffaqiyatli yangilandi!', 'success')
    
    return redirect(url_for('view_bot', bot_id=bot_id))


@app.route('/bot/<int:bot_id>/delete', methods=['POST'])
@login_required
def delete_bot(bot_id):
    """Bot o'chirish"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi o'chira oladi
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botni o\'chirish huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Agar bot ishlayotgan bo'lsa, to'xtatish
    if bot_manager:
        bot_manager.stop_bot(bot_id)
    
    db.session.delete(bot)
    db.session.commit()
    
    flash('Bot o\'chirildi!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/bot/<int:bot_id>/start', methods=['POST'])
@login_required
def start_bot(bot_id):
    """Botni ishga tushirish"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi ishga tushira oladi
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botni ishga tushirish huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Bot manager tekshiruvi va qayta yaratish
    global bot_manager
    if not bot_manager:
        bot_manager = initialize_bot_manager()
        if not bot_manager:
            flash('Bot manager ishlamayapti! Sahifani yangilang.', 'danger')
            return redirect(url_for('view_bot', bot_id=bot_id))
    
    result = bot_manager.start_bot(bot)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')
    
    return redirect(url_for('view_bot', bot_id=bot_id))


@app.route('/bot/<int:bot_id>/stop', methods=['POST'])
@login_required
def stop_bot(bot_id):
    """Botni to'xtatish"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi to'xtata oladi
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botni to\'xtatish huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Bot manager tekshiruvi va qayta yaratish
    global bot_manager
    if not bot_manager:
        bot_manager = initialize_bot_manager()
        if not bot_manager:
            flash('Bot manager ishlamayapti! Sahifani yangilang.', 'danger')
            return redirect(url_for('view_bot', bot_id=bot_id))
    
    result = bot_manager.stop_bot(bot_id)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')
    
    return redirect(url_for('view_bot', bot_id=bot_id))


@app.route('/bot/<int:bot_id>/knowledge')
@login_required
def manage_knowledge(bot_id):
    """Bilimlar bazasini boshqarish"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi ko'ra oladi
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botning bilimlar bazasini ko\'rish huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Bilimlar bazasini yuklash
    from services.knowledge_base import KnowledgeBase
    kb = KnowledgeBase(bot_id, db)
    
    # Yuklangan fayllarni olish
    uploaded_files = kb.get_documents()
    
    # Upload date'ni datetime formatiga o'girish
    for file in uploaded_files:
        if isinstance(file.get('upload_date'), str):
            file['upload_date'] = datetime.fromisoformat(file['upload_date'])
    
    return render_template('manage_knowledge.html',
                         bot=bot,
                         knowledge=kb.knowledge,
                         stats=kb.get_statistics(),
                         uploaded_files=uploaded_files)


@app.route('/bot/<int:bot_id>/knowledge/add', methods=['POST'])
@login_required
def add_knowledge(bot_id):
    """Bilimlar bazasiga ma'lumot qo'shish"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi qo'sha oladi
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botning bilimlar bazasiga qo\'shish huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    from services.knowledge_base import KnowledgeBase
    kb = KnowledgeBase(bot_id, db)
    
    kb_type = request.form.get('type')
    
    try:
        if kb_type == 'faq':
            kb.add_faq(
                question=request.form.get('question'),
                answer=request.form.get('answer')
            )
            flash('Savol-javob qo\'shildi!', 'success')
            
        elif kb_type == 'fact':
            kb.add_fact(
                title=request.form.get('title'),
                content=request.form.get('content')
            )
            flash('Fakt qo\'shildi!', 'success')
            
        elif kb_type == 'instruction':
            steps = request.form.get('steps', '').split('\n')
            kb.add_instruction(
                title=request.form.get('title'),
                steps=[s.strip() for s in steps if s.strip()]
            )
            flash('Ko\'rsatma qo\'shildi!', 'success')
            
        elif kb_type == 'contact':
            kb.add_contact(
                name=request.form.get('name'),
                phone=request.form.get('phone'),
                telegram=request.form.get('telegram'),
                email=request.form.get('email')
            )
            flash('Kontakt qo\'shildi!', 'success')
            
        elif kb_type == 'product':
            kb.add_product(
                name=request.form.get('name'),
                description=request.form.get('description'),
                price=request.form.get('price')
            )
            flash('Mahsulot qo\'shildi!', 'success')
            
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'danger')
    
    return redirect(url_for('manage_knowledge', bot_id=bot_id))


@app.route('/bot/<int:bot_id>/knowledge/delete', methods=['POST'])
@login_required
def delete_knowledge(bot_id):
    """Bilimlar bazasidan o'chirish"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi o'chira oladi
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botning bilimlar bazasidan o\'chirish huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    from services.knowledge_base import KnowledgeBase
    kb = KnowledgeBase(bot_id, db)
    
    kb_type = request.form.get('type')
    item_id = int(request.form.get('item_id'))
    
    try:
        # Ma'lumotni topish va o'chirish
        if kb_type in kb.knowledge:
            items = kb.knowledge[kb_type]
            kb.knowledge[kb_type] = [item for item in items if item.get('id') != item_id]
            kb.save_knowledge()
            flash('Ma\'lumot o\'chirildi!', 'success')
        else:
            flash('Noto\'g\'ri ma\'lumot turi!', 'danger')
            
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'danger')
    
    return redirect(url_for('manage_knowledge', bot_id=bot_id))


@app.route('/bot/<int:bot_id>/knowledge/upload', methods=['POST'])
@login_required
def upload_knowledge_file(bot_id):
    """Bilimlar bazasiga fayl yuklash"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi yuklashi mumkin
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu botga fayl yuklash huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    if 'file' not in request.files:
        flash('Fayl tanlanmagan!', 'danger')
        return redirect(url_for('manage_knowledge', bot_id=bot_id))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Fayl tanlanmagan!', 'danger')
        return redirect(url_for('manage_knowledge', bot_id=bot_id))
    
    # Ruxsat etilgan formatlar
    allowed_extensions = {'txt', 'pdf', 'docx', 'csv', 'xlsx', 'xls'}
    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    if file_ext not in allowed_extensions:
        flash(f'Faqat {", ".join(allowed_extensions).upper()} formatlar ruxsat etilgan!', 'danger')
        return redirect(url_for('manage_knowledge', bot_id=bot_id))
    
    try:
        import os
        from werkzeug.utils import secure_filename
        
        # Upload papkasini yaratish
        upload_folder = f'knowledge/{bot_id}'
        os.makedirs(upload_folder, exist_ok=True)
        
        # Fayl nomini xavfsiz qilish
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        
        # Faylni saqlash
        file.save(filepath)
        
        # Fayl ma'lumotlarini bilim bazasiga qo'shish
        from services.knowledge_base import KnowledgeBase
        kb = KnowledgeBase(bot_id, db)
        
        # Faylni o'qish va qayta ishlash
        file_content = ""
        
        if file_ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                file_content = f.read()
        
        elif file_ext == 'pdf':
            try:
                import PyPDF2
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        file_content += page.extract_text()
            except:
                file_content = "[PDF matni o'qib bo'lmadi]"
        
        elif file_ext == 'docx':
            try:
                from docx import Document
                doc = Document(filepath)
                file_content = '\n'.join([para.text for para in doc.paragraphs])
            except:
                file_content = "[DOCX matni o'qib bo'lmadi]"
        
        elif file_ext in ['csv', 'xlsx', 'xls']:
            try:
                import pandas as pd
                if file_ext == 'csv':
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)
                file_content = df.to_string()
            except:
                file_content = "[Jadval o'qib bo'lmadi]"
        
        # Bilim bazasiga qo'shish
        description = request.form.get('description', '')
        kb.add_document(
            filename=filename,
            content=file_content,
            description=description
        )
        
        flash(f'Fayl muvaffaqiyatli yuklandi: {filename}', 'success')
        
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'danger')
    
    return redirect(url_for('manage_knowledge', bot_id=bot_id))


@app.route('/bot/<int:bot_id>/knowledge/file/<int:file_id>/delete', methods=['POST'])
@login_required
def delete_knowledge_file(bot_id, file_id):
    """Yuklangan faylni o'chirish"""
    bot = Bot.query.get_or_404(bot_id)
    
    # Faqat egasi o'chirishi mumkin
    if bot.user_id != current_user.id and not current_user.is_admin:
        flash('Sizda bu faylni o\'chirish huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        from services.knowledge_base import KnowledgeBase
        kb = KnowledgeBase(bot_id, db)
        kb.delete_document(file_id)
        flash('Fayl o\'chirildi!', 'success')
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'danger')
    
    return redirect(url_for('manage_knowledge', bot_id=bot_id))


# ========== ADMIN ROUTES ==========

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin panel"""
    if not current_user.is_admin:
        flash('Admin huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Statistika
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'premium_users': User.query.filter_by(is_premium=True).count(),
        'total_bots': Bot.query.count(),
        'active_bots': Bot.query.filter_by(is_active=True).count(),
        'today_messages': Message.query.filter(
            Message.created_at >= datetime.utcnow().date()
        ).count()
    }
    
    # So'nggi foydalanuvchilar
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', stats=stats, users=recent_users)


@app.route('/admin/users')
@login_required
def admin_users():
    """Foydalanuvchilar ro'yxati"""
    if not current_user.is_admin:
        flash('Admin huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/user/<int:user_id>/toggle-premium', methods=['POST'])
@login_required
def toggle_premium(user_id):
    """Premium statusni o'zgartirish"""
    if not current_user.is_admin:
        flash('Admin huquqi yo\'q!', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    user.is_premium = not user.is_premium
    db.session.commit()
    
    status = 'Premium' if user.is_premium else 'Test'
    flash(f'{user.username} uchun {status} rejim yoqildi!', 'success')
    return redirect(url_for('admin_users'))


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500


# ========== BOT MANAGER INITIALIZATION ==========

def initialize_bot_manager():
    """Bot manager'ni alohida funksiyada ishga tushirish"""
    global bot_manager
    try:
        bot_manager = BotManager(db)
        print("✅ Bot Manager global o'zgaruvchi tayyor!")
        return bot_manager
    except Exception as e:
        print(f"❌ Bot Manager yaratishda xatolik: {e}")
        import traceback
        traceback.print_exc()
        return None

# Application initialization
def init_app():
    """Application'ni ishga tushirish"""
    with app.app_context():
        # Database jadvallarni yaratish (faqat yangi bo'lsa)
        db.create_all()
        
        # Admin yaratish (agar yo'q bo'lsa)
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@botfactory.uz',
                phone=os.getenv('ADMIN_PHONE'),
                is_admin=True,
                is_premium=True
            )
            admin.set_password(os.getenv('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin yaratildi: username=admin")
        
        # Bot manager'ni ishga tushirish
        initialize_bot_manager()

# Application initialization (Gunicorn uchun ham ishlaydi)
init_app()

# ========== MAIN ==========

if __name__ == '__main__':
    # Production/Development mode
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("🚀 BotFactory ishga tushdi!")
    print(f"📍 Port: {port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
