#!/bin/bash

# Database migratsiya
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Database yaratildi!')
"

# Flask app'ni ishga tushirish
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
