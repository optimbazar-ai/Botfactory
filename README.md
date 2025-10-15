# BotFactory - Flask Web Application

A powerful platform for creating and managing Telegram bots with AI capabilities.

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/botfactory)

## ✨ Features

- 🤖 **Create Smart Bots** - AI-powered chatbots using Google Gemini
- 🎵 **Voice Messages** - Text-to-Speech and Speech-to-Text
- 🌍 **4 Languages** - English, Russian, Uzbek, Spanish
- 📱 **Telegram Integration** - Easy webhook setup
- 🔧 **User-Friendly** - Simple 3-step bot creation
- ⚙️ **Bot Management** - Edit, delete, and manage your bots

## 🚀 Quick Deploy to Netlify

1. **Fork this repository**
2. **Connect to Netlify:**
   - Go to [Netlify](https://netlify.com)
   - Click "New site from Git"
   - Choose your forked repository
3. **Set Environment Variables:**
   - `GOOGLE_API_KEY` - Your Google Gemini API key
   - `SESSION_SECRET` - Random secret key for sessions
4. **Deploy!**

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/botfactory.git
cd botfactory

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
python main.py
```

## 📋 Environment Variables

- `GOOGLE_API_KEY` - Google Gemini API key (required)
- `SESSION_SECRET` - Flask session secret (required)
- `DATABASE_URL` - PostgreSQL URL (optional, defaults to SQLite)

## 🌐 Live Demo

Visit: [Your Netlify URL]

## 📱 How to Use

1. **Register** - Create your free account
2. **Create Bot** - Follow the 3-step process
3. **Get Token** - From @BotFather on Telegram
4. **Set Webhook** - Use the provided HTTPS URL
5. **Test** - Your bot is ready!

## 🔧 Tech Stack

- **Backend:** Flask, SQLAlchemy, SQLite/PostgreSQL
- **AI:** Google Gemini API
- **TTS/STT:** Google Cloud Speech APIs
- **Telegram:** python-telegram-bot
- **Frontend:** Bootstrap 5, Jinja2
- **Deployment:** Netlify Functions

## 📄 License

MIT License - see LICENSE file for details.
- **CSRF Protection**: Flask-WTF for form security
- **Modern UI**: Bootstrap 5 responsive design
- **Subscription Limits**: Free users can create 1 bot (expandable with premium)

## Project Structure

```
botfactory/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── bot.py           # Bot model
│   │   └── knowledge_base.py # Knowledge Base model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── bot.py           # Bot management routes
│   │   ├── kb.py            # Knowledge Base routes
│   │   ├── ai.py            # AI test routes
│   │   └── telegram.py      # Telegram webhook routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py    # Google Gemini integration
│   │   ├── telegram_service.py  # Telegram bot service
│   │   └── kb_service.py    # Knowledge Base file processing
│   ├── templates/
│   │   ├── base.html        # Base template with Bootstrap 5
│   │   ├── index.html       # Home page
│   │   ├── login.html       # Login form
│   │   ├── register.html    # Registration form
│   │   ├── ai/
│   │   │   └── test.html    # AI testing interface
│   │   ├── bots/
│   │   │   ├── list.html    # Bot list view
│   │   │   └── new.html     # Bot creation form
│   │   ├── kb/
│   │   │   ├── manage.html  # Knowledge Base management
│   │   │   └── view.html    # View KB file content
│   │   └── telegram/
│   │       ├── setup.html   # Webhook setup
│   │       └── test.html    # Bot testing interface
│   ├── __init__.py          # App factory
│   └── forms.py             # WTForms (Auth + Bot)
├── config.py                # Configuration
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## User Model

The `User` model includes:
- `id` (int, primary key)
- `username` (str, unique)
- `email` (str, unique)
- `password_hash` (str)
- `language` (str, default: 'uz')
- `subscription_type` (str, default: 'free')
- `is_admin` (bool, default: False)
- `is_active` (bool, default: True)
- `created_at` (datetime)

## Bot Model

The `Bot` model includes:
- `id` (int, primary key)
- `user_id` (int, foreign key to User)
- `name` (str)
- `description` (str, optional)
- `language` (str, choices: uz/ru/en)
- `platform` (str, currently only 'telegram')
- `system_prompt` (text, optional)
- `telegram_token` (str, optional)
- `is_active` (bool, default: True)
- `created_at` (datetime)
- `updated_at` (datetime)

## Knowledge Base Model

The `KnowledgeBase` model includes:
- `id` (int, primary key)
- `bot_id` (int, foreign key to Bot)
- `filename` (str)
- `content` (text) - Extracted text from uploaded file
- `file_type` (str, choices: txt/docx)
- `file_size` (int, bytes)
- `uploaded_at` (datetime)

## Routes

**Authentication:**
- `GET /` - Home page
- `GET /register` - Registration form
- `POST /register` - Create new user
- `GET /login` - Login form
- `POST /login` - Authenticate user
- `GET /logout` - Logout user

**Bot Management (Protected):**
- `GET /bots` - List user's bots
- `GET /bots/new` - Bot creation form
- `POST /bots/new` - Create new bot

**AI Testing (Protected):**
- `GET /ai/test-ai` - AI testing interface
- `POST /ai/test-ai` - Send message to AI
- `POST /ai/test-ai/api` - JSON API endpoint
- `GET /ai/test-connection` - Test Gemini API connection

**Knowledge Base (Protected):**
- `GET /bots/<bot_id>/knowledge-base` - Manage knowledge base files
- `POST /bots/<bot_id>/upload-kb` - Upload .txt or .docx file
- `POST /bots/<bot_id>/kb/<kb_id>/delete` - Delete knowledge base file
- `GET /bots/<bot_id>/kb/<kb_id>/view` - View file content

**Telegram Integration:**
- `POST /telegram/webhook/<bot_id>` - Telegram webhook endpoint (public)
- `GET /telegram/setup/<bot_id>` - Webhook setup page (protected)
- `POST /telegram/setup/<bot_id>` - Set/delete webhook (protected)
- `GET /telegram/test/<bot_id>` - Test bot interface (protected)
- `POST /telegram/test/<bot_id>` - Send test message (protected)

## Installation

1. **Clone the repository** (or navigate to project directory)

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Update `SESSION_SECRET` with a secure random key
   ```bash
   copy .env.example .env
   ```

6. **Run the application**:
   ```bash
   python main.py
   ```

7. **Access the application**:
   - Open browser: http://127.0.0.1:5000

## Environment Variables

Required:
- `SESSION_SECRET`: Flask secret key for sessions (REQUIRED)
- `GOOGLE_API_KEY`: Google Gemini API key for AI features (REQUIRED)

Optional:
- `DATABASE_URL`: PostgreSQL connection string (defaults to SQLite if not set)

### Getting a Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## Database

**SQLite (Default)**: Creates `botfactory.db` in project root

**PostgreSQL (Optional)**: Set `DATABASE_URL` environment variable:
```
DATABASE_URL=postgresql://username:password@localhost/dbname
```

## Security Notes

- Passwords are hashed using bcrypt
- CSRF protection enabled on all forms
- Session secret must be set in environment
- User accounts can be deactivated (is_active flag)
- Bot access is protected by @login_required decorator
- Users can only view/manage their own bots

## Subscription Limits

- **Free Plan**: 1 bot maximum
- **Premium Plans**: Can be configured for unlimited bots

## Next Steps

Planned features:
- **Telegram Webhook Integration**: Connect bots to Telegram API
- **Payment System**: Subscription upgrades (Stripe/PayPal)
- **Admin Dashboard**: User and bot management for admins
- **Bot Analytics**: Track usage and conversations
- **Edit/Delete Bots**: Full CRUD operations for bot management
- **Multi-language UI**: Uzbek/Russian/English interface support
- **Connect AI to Bots**: Use bot's system_prompt with Telegram messages

## Dependencies

- Flask 3.1.2
- Flask-Login 0.6.3
- Flask-WTF 1.2.1
- Flask-SQLAlchemy 3.1.1
- bcrypt 4.1.2
- python-dotenv 1.0.1
- psycopg2-binary 2.9.9
- email-validator 2.1.0
- google-generativeai 0.8.3
- python-telegram-bot 22.0.0
- python-docx 1.1.2

## Documentation

- **README.md** - Main documentation (this file)
- **AI_INTEGRATION.md** - Google Gemini AI setup and usage
- **TELEGRAM_INTEGRATION.md** - Telegram bot webhook guide
- **USAGE.md** - User guide for the application
- **CHANGELOG.md** - Version history and changes
