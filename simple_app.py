"""
Minimal Flask app - xatoliklarni topish uchun
"""
import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

@app.route('/')
def index():
    return """
    <h1>🎉 BotFactory Test</h1>
    <p>Agar bu sahifani ko'rayotgan bo'lsangiz, Flask ishlayapti!</p>
    <a href="/test">Test sahifasi</a>
    """

@app.route('/test')
def test():
    return """
    <h2>✅ Test muvaffaqiyatli!</h2>
    <p>Flask to'liq ishlayapti</p>
    <a href="/">Bosh sahifa</a>
    """

@app.route('/bots/')
def bots():
    return """
    <h2>🤖 Botlar sahifasi</h2>
    <p>Bu yerda botlar bo'ladi</p>
    <a href="/">Bosh sahifa</a>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
