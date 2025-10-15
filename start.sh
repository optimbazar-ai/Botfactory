#!/bin/bash

echo "🚀 BotFactory ishga tushmoqda..."

# Flask app'ni ishga tushirish (bot manager avtomatik ishga tushadi)
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --log-level info
