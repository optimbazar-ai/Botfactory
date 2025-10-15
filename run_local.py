"""
Local development uchun Flask app ishga tushirish
"""
import os
from app import create_app

# Environment variables
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('SESSION_SECRET', 'local-dev-secret-key-2024')

app = create_app()

if __name__ == '__main__':
    print("🚀 BotFactory Local Development Server")
    print("📱 URL: http://localhost:5000")
    print("🔧 Debug mode: ON")
    print("💡 Webhook test uchun ngrok kerak bo'ladi")
    print("-" * 50)
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
