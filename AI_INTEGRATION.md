# Google Gemini AI Integration Guide

## Overview

BotFactory now integrates with Google Gemini 1.5 Flash model for intelligent AI responses. The AI service supports multi-language auto-detection and can respond in Uzbek, Russian, or English.

## Features

✅ **Multi-language Support**: Auto-detects input language (uz/ru/en) and responds in the same language  
✅ **Custom System Prompts**: Configure AI behavior with custom instructions  
✅ **Plain Text Responses**: No markdown formatting, clean text output  
✅ **Emoji Support**: Friendly responses with appropriate emojis  
✅ **Error Handling**: Graceful fallback messages when API fails  
✅ **Test Interface**: Web-based testing page at `/ai/test-ai`

## Setup

### 1. Get Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated API key

### 2. Configure Environment

Add to your `.env` file:

```env
GOOGLE_API_KEY=your-api-key-here
```

⚠️ **Important**: The application will not start without this key.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `google-generativeai==0.8.3` along with other dependencies.

## Using the AI Service

### Function Signature

```python
from app.services.ai_service import get_gemini_response

response = get_gemini_response(
    user_message: str,          # Required: User's input
    system_prompt: str = None,  # Optional: AI behavior instructions
    language: str = 'uz'        # Optional: Fallback language
)
```

### Example Usage

```python
# Simple message (auto-detects language)
response = get_gemini_response("Salom! Qalaysiz?")
# Response: "Salom! Men yaxshiman, rahmat! Sizchi? 😊"

# With custom system prompt
response = get_gemini_response(
    user_message="Write a haiku about coding",
    system_prompt="You are a creative poet who loves programming"
)

# Specify fallback language
response = get_gemini_response(
    user_message="Hello!",
    language='en'
)
```

## Web Testing Interface

### Access the Test Page

1. **Login** to your account
2. Navigate to **"Test AI"** in the navbar
3. Or visit: `http://127.0.0.1:5000/ai/test-ai`

### Test Page Features

- **Message Input**: Type your message in any supported language
- **System Prompt**: Optional custom instructions for AI behavior
- **Language Selector**: Choose fallback language (uz/ru/en)
- **Real-time Response**: See AI responses immediately
- **Example Prompts**: Pre-made examples to try

### API Endpoints

#### POST /ai/test-ai
Form-based endpoint (returns HTML)

**Form Parameters:**
- `message` (required): User's message
- `system_prompt` (optional): Custom system prompt
- `language` (optional): Fallback language (uz/ru/en)

#### POST /ai/test-ai/api
JSON API endpoint

**Request Body:**
```json
{
    "message": "Your message here",
    "system_prompt": "Optional system prompt",
    "language": "uz"
}
```

**Response:**
```json
{
    "success": true,
    "user_message": "Your message here",
    "ai_response": "AI's response",
    "language": "uz"
}
```

#### GET /ai/test-connection
Test if Gemini API is configured correctly

**Response:**
```json
{
    "success": true,
    "message": "Gemini API is working!"
}
```

## Language Auto-Detection

The AI automatically detects the input language:

- **Uzbek Input** → Responds in Uzbek
  ```
  User: "Salom! Bugun havo qanday?"
  AI: "Salom! Men sun'iy intellekt assistentiman..."
  ```

- **Russian Input** → Responds in Russian
  ```
  User: "Привет! Как дела?"
  AI: "Привет! Я искусственный интеллект..."
  ```

- **English Input** → Responds in English
  ```
  User: "Hello! How are you?"
  AI: "Hello! I'm an AI assistant..."
  ```

## Error Handling

The service includes graceful error handling:

### API Errors
If the Gemini API fails (network issues, rate limits, invalid key), the service returns a friendly fallback message in the appropriate language:

- **Uzbek**: "Kechirasiz, hozirda javob bera olmayapman. Iltimos, keyinroq urinib ko'ring. 😊"
- **Russian**: "Извините, я не могу ответить прямо сейчас. Пожалуйста, попробуйте позже. 😊"
- **English**: "Sorry, I cannot respond right now. Please try again later. 😊"

### Common Issues

**"GOOGLE_API_KEY environment variable is required"**
- Solution: Add `GOOGLE_API_KEY` to your `.env` file

**Rate Limit Exceeded**
- Gemini has usage limits on the free tier
- Wait a few minutes before trying again
- Consider upgrading to paid tier for higher limits

**Connection Errors**
- Check your internet connection
- Verify API key is correct
- Test connection at `/ai/test-connection`

## Technical Details

### Model
- **Model Name**: `gemini-1.5-flash`
- **Provider**: Google AI (Gemini)
- **Response Format**: Plain text (markdown removed)

### Text Processing
The service automatically:
- Removes markdown formatting (`**bold**`, `*italic*`, `` `code` ``)
- Removes headers (`#`, `##`, `###`)
- Preserves emojis and special characters
- Trims whitespace

### Service Functions

#### `get_gemini_response()`
Main function for getting AI responses.

#### `test_gemini_connection()`
Tests if the API is configured correctly.

#### `_get_fallback_message()`
Returns error message in appropriate language.

## Integration with Bots

🚧 **Coming Soon**: Direct integration with Telegram bots

The AI service is ready to be connected to your bots. Future updates will:
1. Use the bot's `system_prompt` field for AI behavior
2. Process Telegram messages through the AI
3. Send AI responses back to users
4. Track conversation history

## Best Practices

### System Prompts

Good system prompts are:
- **Clear**: "You are a customer support assistant for a tech company"
- **Specific**: "Answer only questions about Python programming"
- **Contextual**: "You are helping users learn Uzbek language"

Avoid:
- ❌ Too vague: "Be helpful"
- ❌ Too long: (over 2000 characters)
- ❌ Conflicting instructions

### Rate Limiting

Free tier limits:
- 60 requests per minute
- 1,500 requests per day

Tips:
- Cache common responses
- Implement request throttling
- Monitor usage in Google AI Studio

### Security

- ✅ Never expose `GOOGLE_API_KEY` in code
- ✅ Keep `.env` file in `.gitignore`
- ✅ Use environment variables only
- ✅ Rotate keys periodically
- ❌ Don't commit API keys to Git
- ❌ Don't share keys publicly

## Testing Examples

### Example 1: Simple Conversation
```
Message: "Salom! O'zingni tanishtirib ber"
System Prompt: (empty)
Language: uz

AI Response: "Salom! Men sun'iy intellekt yordamchisiman. 
Men savollaringizga javob berish va sizga yordam berishga 
tayyorman. Nimada yordam bera olaman? 😊"
```

### Example 2: Role-Based
```
Message: "Explain variables"
System Prompt: "You are a Python programming teacher"
Language: en

AI Response: "Variables in Python are containers that store 
data values. You can think of them as labeled boxes where 
you put information..."
```

### Example 3: Multi-language
```
Message: "Как создать переменную в Python?"
System Prompt: "You are a programming tutor"
Language: ru

AI Response: "Чтобы создать переменную в Python, просто 
присвойте значение имени. Например: x = 10 или name = 'Ivan'..."
```

## API Reference

### Configuration (config.py)
```python
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required")
```

### Service Module (app/services/ai_service.py)
```python
get_gemini_response(user_message, system_prompt=None, language='uz')
test_gemini_connection()
```

### Routes (app/routes/ai.py)
```python
GET  /ai/test-ai           # Web interface
POST /ai/test-ai           # Form submission
POST /ai/test-ai/api       # JSON API
GET  /ai/test-connection   # Connection test
```

## Troubleshooting

### Issue: API Key Not Working
1. Check if key is correct in `.env`
2. Restart the Flask application
3. Test at `/ai/test-connection`
4. Generate new key if needed

### Issue: Responses Are in Wrong Language
- The AI auto-detects language from input
- Make sure your message is clearly in one language
- Use `language` parameter as fallback

### Issue: Markdown Still Appearing
- The service removes common markdown
- Some complex formatting might remain
- Report as issue if persistent

## Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Python SDK Documentation](https://ai.google.dev/tutorials/python_quickstart)
- [Rate Limits & Pricing](https://ai.google.dev/pricing)

## Support

For issues with:
- **AI Integration**: Check this guide
- **API Keys**: Visit Google AI Studio
- **Rate Limits**: Check your usage dashboard
- **Application**: Check main README.md
