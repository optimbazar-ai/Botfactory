import os
import google.generativeai as genai
from flask import current_app


def get_gemini_response(user_message: str, system_prompt: str = None, language: str = 'uz', knowledge_base_text: str = None) -> str:
    """
    Get response from Google Gemini AI model.
    
    Args:
        user_message: The user's input message
        system_prompt: Optional system prompt to guide the AI's behavior
        language: User's preferred language (uz/ru/en) - auto-detected from input
        knowledge_base_text: Optional knowledge base context to use for answering
        
    Returns:
        str: AI response in plain text (no markdown)
    """
    try:
        # Configure Gemini API
        genai.configure(api_key=current_app.config['GOOGLE_API_KEY'])
        
        # Initialize the model (using gemini-2.5-flash - stable version)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Build the prompt with specific language instruction
        language_names = {
            'en': 'English',
            'ru': 'Russian (Русский язык)',
            'uz': 'Uzbek (O\'zbek tili)',
            'es': 'Spanish (Español)'
        }
        
        language_instruction = f"""
IMPORTANT: You MUST respond in {language_names.get(language, 'Uzbek')} language ONLY.
- User's preferred language: {language}
- Respond in {language_names.get(language, 'Uzbek')} regardless of what language the user writes in
- Use emojis where appropriate to make the conversation friendly
- Provide plain text responses without markdown formatting
- Do NOT translate - just respond naturally in {language_names.get(language, 'Uzbek')}
"""
        
        # Build knowledge base context if provided
        kb_context = ""
        if knowledge_base_text:
            kb_context = f"""
Use the following context/knowledge base to answer the user's question. 
If the answer is in the knowledge base, use it. If not, provide a general helpful response.

KNOWLEDGE BASE:
{knowledge_base_text}

---
"""
        
        # Combine system prompt with knowledge base and language instruction
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{kb_context}{language_instruction}\n\nUser: {user_message}"
        else:
            # Default helpful assistant behavior
            default_system = "You are a helpful, friendly assistant."
            full_prompt = f"{default_system}\n\n{kb_context}{language_instruction}\n\nUser: {user_message}"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        # Extract text from response
        if response and response.text:
            # Remove markdown formatting and clean up
            ai_response = response.text.strip()
            
            # Remove common markdown patterns
            ai_response = ai_response.replace('**', '')  # Bold
            ai_response = ai_response.replace('*', '')   # Italic
            ai_response = ai_response.replace('`', '')   # Code
            ai_response = ai_response.replace('###', '') # Headers
            ai_response = ai_response.replace('##', '')
            ai_response = ai_response.replace('#', '')
            
            return ai_response
        else:
            return _get_fallback_message(language)
            
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Gemini API Error: {str(e)}")
        
        # Return a graceful fallback message
        return _get_fallback_message(language)


def _get_fallback_message(language: str) -> str:
    """
    Get fallback message when AI service fails.
    
    Args:
        language: User's preferred language
        
    Returns:
        str: Error message in the appropriate language
    """
    fallback_messages = {
        'en': "Sorry, I cannot respond right now. Please try again later. 😊",
        'ru': "Извините, я не могу ответить прямо сейчас. Пожалуйста, попробуйте позже. 😊",
        'uz': "Kechirasiz, hozirda javob bera olmayapman. Iltimos, keyinroq urinib ko'ring. 😊",
        'es': "Lo siento, no puedo responder en este momento. Por favor, inténtalo más tarde. 😊"
    }
    
    return fallback_messages.get(language, fallback_messages['en'])


def test_gemini_connection() -> bool:
    """
    Test if Gemini API is configured correctly.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        genai.configure(api_key=current_app.config['GOOGLE_API_KEY'])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Send a simple test message
        response = model.generate_content("Say 'OK' if you can read this.")
        
        return response and response.text and len(response.text) > 0
    except Exception as e:
        print(f"Gemini Connection Test Failed: {str(e)}")
        return False
