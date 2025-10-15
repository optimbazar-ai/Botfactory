"""
Netlify deployment entry point
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
from main import app

# Export app for Netlify
application = app

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)
