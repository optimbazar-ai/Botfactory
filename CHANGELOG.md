# Changelog

## [Latest] - 2025-10-05

### Added - Knowledge Base Feature

#### New Models
- **KnowledgeBase Model** (`app/models/knowledge_base.py`)
  - Fields: id, bot_id, filename, content, file_type, file_size, uploaded_at
  - Foreign key relationship to Bot model
  - Supports .txt and .docx file formats
  - Maximum file size: 16 MB

#### New Services
- **KB Service** (`app/services/kb_service.py`)
  - `process_uploaded_file()` - Extract text from .txt/.docx files
  - `extract_text_from_txt()` - Process text files
  - `extract_text_from_docx()` - Process Word documents
  - `combine_knowledge_bases()` - Merge multiple KB files
  - File validation (type, size)

#### New Routes
- **KB Blueprint** (`app/routes/kb.py`)
  - `GET /bots/<bot_id>/knowledge-base` - KB management page
  - `POST /bots/<bot_id>/upload-kb` - Upload KB file
  - `POST /bots/<bot_id>/kb/<kb_id>/delete` - Delete KB file
  - `GET /bots/<bot_id>/kb/<kb_id>/view` - View KB content

#### New Templates
- **KB Management** (`app/templates/kb/manage.html`)
  - Upload form for .txt/.docx files
  - List of uploaded KB files
  - File information display
  - Usage examples and instructions

- **KB Viewer** (`app/templates/kb/view.html`)
  - View file content
  - File metadata
  - Delete action

#### Updated Services
- **AI Service** (`app/services/ai_service.py`)
  - Added `knowledge_base_text` parameter to `get_gemini_response()`
  - KB context injection into AI prompts
  - Automatic KB usage when available

- **Telegram Service** (`app/services/telegram_service.py`)
  - Automatically loads bot's knowledge bases
  - Combines multiple KB files
  - Passes KB to AI for context-aware responses

#### Updated Templates
- **Bot List** (`app/templates/bots/list.html`)
  - Added "📚 Knowledge Base" button for each bot

#### Dependencies
- Added `python-docx==1.1.2` for .docx file processing

#### Features
✅ **File Upload** - Support for .txt and .docx files (max 16MB)
✅ **Text Extraction** - Automatic text extraction from documents
✅ **Multiple Files** - Upload and combine multiple KB files
✅ **AI Integration** - KB context automatically used in AI responses
✅ **File Management** - View, list, and delete KB files
✅ **Validation** - File type and size validation
✅ **UTF-8 Support** - Proper encoding handling

#### Use Cases
- FAQ documents for customer support bots
- Product information and specifications
- Company policies and procedures
- Technical documentation
- Training materials and tutorials

---

## [Previous] - 2025-10-05

### Added - Telegram Webhook Integration

#### New Services
- **Telegram Service** (`app/services/telegram_service.py`)
  - `process_telegram_message()` - Process incoming messages
  - `set_webhook()` - Configure Telegram webhook
  - `delete_webhook()` - Remove webhook
  - `get_bot_info()` - Get bot information
  - `send_typing_action()` - Show typing indicator
  - `run_async()` - Helper for async operations in Flask

#### New Routes
- **Telegram Blueprint** (`app/routes/telegram.py`)
  - `POST /telegram/webhook/<bot_id>` - Webhook endpoint for Telegram
  - `GET/POST /telegram/setup/<bot_id>` - Webhook management UI
  - `GET/POST /telegram/test/<bot_id>` - Bot testing interface

#### New Templates
- **Webhook Setup** (`app/templates/telegram/setup.html`)
  - Bot information display
  - Webhook status and management
  - ngrok setup instructions
  - Production deployment guide

- **Bot Testing** (`app/templates/telegram/test.html`)
  - Test bot without webhook
  - Simulate Telegram messages
  - View AI responses
  - Bot configuration display

#### Updated Templates
- **Bot List** (`app/templates/bots/list.html`)
  - Added "Webhook Setup" button
  - Added "Test Bot" button
  - Shows setup required warning

#### Dependencies
- Added `python-telegram-bot==22.0.0`

#### Documentation
- **TELEGRAM_INTEGRATION.md** - Comprehensive guide
  - Setup instructions
  - ngrok tutorial
  - Production deployment
  - Troubleshooting
  - Code examples
  - FAQ

#### Features
✅ **Full Webhook Support** - Receive messages from Telegram
✅ **AI Integration** - Responses powered by Google Gemini
✅ **Typing Indicator** - Shows "typing..." before response
✅ **Multi-language** - Auto-detects user language
✅ **System Prompts** - Each bot uses its own system prompt
✅ **Test Interface** - Test without setting up webhook
✅ **Webhook Management** - Easy UI for setup/delete
✅ **ngrok Support** - Local testing guide included

---

## [Previous] - 2025-10-05

### Added - Bot Management System

#### New Models
- **Bot Model** (`app/models/bot.py`)
  - Fields: id, user_id, name, description, language, platform, system_prompt, telegram_token, is_active, created_at, updated_at
  - Foreign key relationship to User model
  - Support for Telegram platform (expandable to other platforms)

#### New Routes
- **Bot Blueprint** (`app/routes/bot.py`)
  - `GET /bots` - List all bots for current user (login required)
  - `GET /bots/new` - Bot creation form (login required)
  - `POST /bots/new` - Create new bot with validation (login required)
  - Subscription limit enforcement (free users: 1 bot max)

#### New Forms
- **BotForm** (`app/forms.py`)
  - Name field (required, 3-100 chars)
  - Description field (optional, max 500 chars)
  - Language dropdown (uz/ru/en)
  - Platform dropdown (telegram only for now)
  - System prompt textarea (optional, max 2000 chars)
  - Telegram token field (optional)
  - Full validation and error handling

#### New Templates
- **Bot List Page** (`app/templates/bots/list.html`)
  - Grid view of all user's bots
  - Shows bot status, platform, language, token status
  - Subscription limit warning for free users
  - Empty state with call-to-action
  - Placeholder action buttons (View/Edit/Delete - coming soon)

- **Bot Creation Page** (`app/templates/bots/new.html`)
  - Form with all bot fields
  - Bootstrap validation styling
  - Help text and links to @BotFather
  - Cancel button to return to list
  - Information about upcoming features

#### UI Updates
- **Navigation Bar** (`app/templates/base.html`)
  - Added "My Bots" link (visible when logged in)
  - Better menu structure with left and right aligned items

- **Home Page** (`app/templates/index.html`)
  - Added "Manage Bots" and "Create New Bot" buttons for authenticated users
  - Quick access to bot management features

#### Application Updates
- **App Factory** (`app/__init__.py`)
  - Registered bot blueprint
  - Auto-creates bot table on startup

#### Documentation
- **README.md** - Updated with:
  - Bot model documentation
  - New routes documentation
  - Updated project structure
  - Bot management features
  - Subscription limits section
  - Updated next steps

- **USAGE.md** - New comprehensive guide with:
  - Setup instructions
  - Step-by-step bot creation
  - Telegram token guide
  - Subscription limits explanation
  - Troubleshooting section
  - Security best practices

- **CHANGELOG.md** - This file

### Features

✅ **Bot CRUD** (Create and Read implemented, Update and Delete planned)
✅ **Subscription Limits** - Free users limited to 1 bot
✅ **Protected Routes** - All bot routes require authentication
✅ **User Isolation** - Users can only see/manage their own bots
✅ **Form Validation** - Comprehensive validation with error messages
✅ **Responsive UI** - Bootstrap 5 cards and forms
✅ **Empty States** - Friendly UI when no bots exist

### Limitations / Not Yet Implemented

❌ Edit bot functionality
❌ Delete bot functionality
❌ Telegram webhook integration
❌ AI integration for bot responses
❌ Payment/subscription system
❌ Bot analytics
❌ Admin dashboard
❌ Multi-language UI (data only, UI still in English)

### Technical Details

- **Database**: SQLAlchemy relationship between User and Bot (one-to-many)
- **Validation**: WTForms with custom validators
- **Security**: @login_required decorator on all bot routes
- **UI Framework**: Bootstrap 5.3.2 via CDN
- **Form Protection**: Flask-WTF CSRF tokens on all forms

### File Changes

**New Files:**
- `app/models/bot.py`
- `app/routes/bot.py`
- `app/templates/bots/list.html`
- `app/templates/bots/new.html`
- `USAGE.md`
- `CHANGELOG.md`

**Modified Files:**
- `app/__init__.py` - Registered bot blueprint
- `app/forms.py` - Added BotForm and new imports
- `app/templates/base.html` - Added bot navigation link
- `app/templates/index.html` - Added bot management buttons
- `README.md` - Updated documentation

**Unchanged Files:**
- `app/models/user.py` - No changes (relationship defined in bot.py)
- `app/routes/auth.py` - No changes
- `config.py` - No changes
- `main.py` - No changes
- `requirements.txt` - No new dependencies needed

### Database Schema Changes

New table: `bots`
```sql
CREATE TABLE bots (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    language VARCHAR(10) NOT NULL DEFAULT 'uz',
    platform VARCHAR(20) NOT NULL DEFAULT 'telegram',
    system_prompt TEXT,
    telegram_token VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

### Migration Notes

No manual migration needed. SQLAlchemy will auto-create the `bots` table on next run via `db.create_all()`.

Existing users and data will not be affected.
