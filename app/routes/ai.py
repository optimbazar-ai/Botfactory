from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.services.ai_service import get_gemini_response, test_gemini_connection

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


@ai_bp.route('/test-ai', methods=['GET', 'POST'])
@login_required
def test_ai():
    """Test route for AI functionality."""
    response_data = None
    error = None
    
    if request.method == 'POST':
        # Get parameters from form
        user_message = request.form.get('message', '').strip()
        system_prompt = request.form.get('system_prompt', '').strip()
        language = request.form.get('language', 'uz')
        
        if not user_message:
            error = "Please enter a message"
        else:
            # Get AI response
            ai_response = get_gemini_response(
                user_message=user_message,
                system_prompt=system_prompt if system_prompt else None,
                language=language
            )
            
            response_data = {
                'user_message': user_message,
                'system_prompt': system_prompt,
                'language': language,
                'ai_response': ai_response
            }
    
    return render_template('ai/test.html', response=response_data, error=error)


@ai_bp.route('/test-ai/api', methods=['POST'])
@login_required
def test_ai_api():
    """API endpoint for testing AI (returns JSON)."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data.get('message', '').strip()
        system_prompt = data.get('system_prompt', '').strip()
        language = data.get('language', 'uz')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get AI response
        ai_response = get_gemini_response(
            user_message=user_message,
            system_prompt=system_prompt if system_prompt else None,
            language=language
        )
        
        return jsonify({
            'success': True,
            'user_message': user_message,
            'ai_response': ai_response,
            'language': language
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_bp.route('/test-connection')
@login_required
def test_connection():
    """Test if Gemini API is working."""
    is_connected = test_gemini_connection()
    
    return jsonify({
        'success': is_connected,
        'message': 'Gemini API is working!' if is_connected else 'Failed to connect to Gemini API'
    })
