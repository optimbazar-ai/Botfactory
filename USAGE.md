# BotFactory Usage Guide

## Quick Start

### 1. Setup Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env and set your SESSION_SECRET
# SESSION_SECRET=your-secure-random-key-here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

The application will start at: http://127.0.0.1:5000

## Using the Bot Management System

### Step 1: Register an Account

1. Navigate to http://127.0.0.1:5000
2. Click **"Register"** in the navigation bar
3. Fill in:
   - Username (3-80 characters)
   - Email address
   - Password (minimum 6 characters)
   - Confirm password
4. Click **"Register"**

### Step 2: Login

1. Click **"Login"** in the navigation bar
2. Enter your username and password
3. Click **"Login"**

### Step 3: Create Your First Bot

1. After logging in, you'll see buttons on the home page
2. Click **"Create New Bot"** or navigate to **"My Bots"** → **"Create New Bot"**
3. Fill in the bot details:
   - **Bot Name**: Give your bot a descriptive name (required)
   - **Description**: Brief description of what your bot does (optional)
   - **Language**: Choose Uzbek, Russian, or English
   - **Platform**: Currently only Telegram is supported
   - **System Prompt**: Instructions for the AI (optional, for future AI integration)
   - **Telegram Bot Token**: Get from [@BotFather](https://t.me/BotFather) (optional)
4. Click **"Create Bot"**

### Step 4: View Your Bots

1. Click **"My Bots"** in the navigation bar
2. You'll see all your bots with:
   - Bot name and status (Active/Inactive)
   - Description
   - Platform and language
   - Token configuration status
   - Creation date

## Subscription Limits

### Free Plan (Default)
- **Maximum Bots**: 1
- If you try to create a second bot, you'll see an error message
- Upgrade option will be available in future versions

### Premium Plans (Coming Soon)
- Unlimited bots
- Advanced AI features
- Priority support

## Bot Configuration Fields

### Required Fields
- **Name**: Your bot's display name
- **Language**: Interface language (uz/ru/en)
- **Platform**: Currently only Telegram

### Optional Fields
- **Description**: What your bot does
- **System Prompt**: AI behavior instructions (for future AI integration)
- **Telegram Token**: From @BotFather (required for Telegram integration)

## Getting a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the prompts:
   - Choose a name for your bot
   - Choose a username (must end with 'bot')
4. @BotFather will send you a token that looks like:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
5. Copy this token and paste it in the **Telegram Bot Token** field when creating your bot

## Current Limitations

🚧 **Work in Progress** - The following features are not yet implemented:

- ❌ Telegram webhook integration (bot won't respond to messages yet)
- ❌ AI integration (no automated responses yet)
- ❌ Edit bot functionality
- ❌ Delete bot functionality
- ❌ Bot analytics and statistics
- ❌ Payment/subscription system

These features are planned for future releases.

## Troubleshooting

### "SESSION_SECRET environment variable is required"
- Make sure you've created a `.env` file
- Ensure `SESSION_SECRET` is set in the `.env` file

### "You have reached the maximum number of bots for free plan"
- Free users can only create 1 bot
- Delete your existing bot or wait for premium subscription feature

### Database not created
- The SQLite database is created automatically on first run
- Check for `botfactory.db` file in the project root
- Make sure you have write permissions in the project directory

## Database Management

### Using SQLite (Default)
- Database file: `botfactory.db` in project root
- Automatically created on first run
- Good for development and small deployments

### Using PostgreSQL
Set the `DATABASE_URL` environment variable in `.env`:
```
DATABASE_URL=postgresql://username:password@localhost/botfactory
```

### Reset Database
To start fresh, simply delete `botfactory.db` and restart the app.

## Security Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use strong SESSION_SECRET** - Generate a random string
3. **Keep bot tokens secure** - Don't share or commit them
4. **Use strong passwords** - Minimum 6 characters (recommended: 12+)

## File Structure Overview

```
/app
  /models
    bot.py          # Bot database model
    user.py         # User database model
  /routes
    auth.py         # Login/register routes
    bot.py          # Bot management routes
  /templates
    /bots
      list.html     # Shows all your bots
      new.html      # Create new bot form
    base.html       # Template with navbar
    index.html      # Home page
    login.html      # Login page
    register.html   # Registration page
  __init__.py       # App initialization
  forms.py          # Form definitions

main.py             # App entry point
config.py           # Configuration
requirements.txt    # Dependencies
.env                # Environment variables (create this)
```

## Next Steps

After setting up your bot, you can:
1. Wait for AI integration features
2. Wait for Telegram webhook setup
3. Prepare your system prompts for when AI is integrated
4. Get your Telegram token ready

## Support

For issues or questions:
- Check this usage guide
- Review README.md for technical details
- Check error messages in the browser and console
