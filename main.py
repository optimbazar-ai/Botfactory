"""
Minimal Flask app - xatoliklarni topish uchun
"""
import os
from flask import Flask

print("🚀 BotFactory minimal app ishga tushmoqda...")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'fallback-secret-key')

@app.route('/')
def index():
    print("📱 Bosh sahifa so'raldi")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BotFactory - Test</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; margin: 50px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #007bff; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 BotFactory Test Sahifasi</h1>
            <p>Agar bu sahifani ko'rayotgan bo'lsangiz, Flask muvaffaqiyatli ishlayapti!</p>
            <p><a href="/test" class="btn">Test sahifasi</a></p>
            <p><a href="/bots/" class="btn">Botlar sahifasi</a></p>
            <hr>
            <p><small>Render.com'da deploy qilindi ✅</small></p>
        </div>
    </body>
    </html>
    """

@app.route('/test')
def test():
    print("🧪 Test sahifasi so'raldi")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test - BotFactory</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; margin: 50px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h2 { color: #28a745; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>✅ Test Muvaffaqiyatli!</h2>
            <p>Flask to'liq ishlayapti va sahifalar render qilinmoqda</p>
            <p><a href="/" class="btn">Bosh sahifa</a></p>
        </div>
    </body>
    </html>
    """

@app.route('/bots/')
def bots():
    print("🤖 Botlar sahifasi so'raldi")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Botlar - BotFactory</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; margin: 50px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h2 { color: #6f42c1; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🤖 Botlar Sahifasi</h2>
            <p>Bu yerda botlar ro'yxati bo'ladi</p>
            <p>Hozircha test rejimida ishlamoqda</p>
            <p><a href="/" class="btn">Bosh sahifa</a></p>
        </div>
    </body>
    </html>
    """

@app.errorhandler(404)
def not_found(error):
    print(f"❌ 404 xatolik: {error}")
    return """
    <h1>404 - Sahifa topilmadi</h1>
    <p><a href="/">Bosh sahifaga qaytish</a></p>
    """, 404

@app.errorhandler(500)
def server_error(error):
    print(f"❌ 500 xatolik: {error}")
    return """
    <h1>500 - Server xatoligi</h1>
    <p>Nimadir noto'g'ri ketdi</p>
    <p><a href="/">Bosh sahifaga qaytish</a></p>
    """, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Server {port} portda ishga tushmoqda...")
    app.run(debug=False, host='0.0.0.0', port=port)
