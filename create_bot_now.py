"""
Bot yaratish va darhol ishga tushirish
"""
import sqlite3
from datetime import datetime

# Bot ma'lumotlari
bot_name = "Test Bot"
bot_token = "7568964660:AAHx_cinhFhE9yo-iBmyJKjikr7iQYA8VgY"
bot_username = "meningchatbotim_bot"
admin_chat_id = "1021369075"

# Database'ga yozish
conn = sqlite3.connect('instance/botfactory.db')
cursor = conn.cursor()

# Admin user ID olish
cursor.execute("SELECT id FROM users WHERE username='admin' LIMIT 1")
user = cursor.fetchone()

if not user:
    print("❌ Admin user topilmadi!")
else:
    user_id = user[0]
    print(f"✅ Admin user ID: {user_id}")
    
    # Bot qo'shish
    cursor.execute("""
        INSERT INTO bots (
            user_id, name, description, telegram_token, 
            telegram_username, language, system_prompt, 
            is_active, admin_chat_id, notification_channel,
            notifications_enabled, total_messages, today_messages, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        bot_name,
        "BotFactory orqali yaratilgan test bot",
        bot_token,
        bot_username,
        'uz',
        "Siz yordam beruvchi virtual assistentsiz. Foydalanuvchi savollariga o'zbek tilida aniq va foydali javoblar bering.",
        1,  # is_active = True
        admin_chat_id,
        None,  # notification_channel
        1,  # notifications_enabled = True
        0,  # total_messages
        0,  # today_messages
        datetime.now()
    ))
    
    conn.commit()
    bot_id = cursor.lastrowid
    
    print(f"✅ BOT YARATILDI!")
    print(f"   ID: {bot_id}")
    print(f"   Nomi: {bot_name}")
    print(f"   Username: @{bot_username}")
    print(f"   Admin Chat: {admin_chat_id}")
    print(f"   Status: FAOL")

conn.close()

print("\n🚀 ENDI TELEGRAM'DA TEST QILING:")
print(f"1. @{bot_username} ga o'ting")
print("2. /start yuboring")
print("3. Bot javob berishi kerak!")
