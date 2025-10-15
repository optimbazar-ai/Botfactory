"""
Local bot test - webhook'siz test qilish
"""
import os
import sys
import asyncio
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.telegram_service import handle_message
from app.models.bot import BotModel

def test_bot_locally():
    """
    Bot'ni local test qilish - webhook'siz
    """
    app = create_app()
    
    with app.app_context():
        print("🤖 Local Bot Test")
        print("=" * 40)
        
        # Get all bots
        bots = BotModel.query.all()
        
        if not bots:
            print("❌ Hech qanday bot topilmadi!")
            print("💡 Avval saytda bot yarating: http://localhost:5000")
            return
        
        print(f"📋 {len(bots)} ta bot topildi:")
        for i, bot in enumerate(bots, 1):
            print(f"   {i}. {bot.name} (ID: {bot.id})")
        
        # Select bot
        try:
            bot_num = int(input("\n🎯 Qaysi botni test qilmoqchisiz? (raqam): "))
            selected_bot = bots[bot_num - 1]
        except (ValueError, IndexError):
            print("❌ Noto'g'ri raqam!")
            return
        
        print(f"\n✅ Tanlangan bot: {selected_bot.name}")
        
        # Check bot tokens
        tokens = selected_bot.get_telegram_tokens()
        if not tokens:
            print("❌ Bot'da Telegram token yo'q!")
            print("💡 Botni tahrirlang va token qo'shing")
            return
        
        print(f"🔑 Token mavjud: {tokens[0][:10]}...")
        
        # Test message
        print("\n" + "="*40)
        print("💬 Test xabar yuboring (exit - chiqish):")
        
        while True:
            user_message = input("\n👤 Siz: ")
            
            if user_message.lower() in ['exit', 'quit', 'chiqish']:
                break
            
            if not user_message.strip():
                continue
            
            # Simulate Telegram message
            fake_message = {
                'message_id': 123,
                'from': {
                    'id': 12345,
                    'first_name': 'Test User',
                    'username': 'testuser'
                },
                'chat': {
                    'id': 12345,
                    'type': 'private'
                },
                'text': user_message,
                'date': int(datetime.now().timestamp())
            }
            
            print("🤖 Bot javob tayyorlamoqda...")
            
            try:
                # Test bot response
                result = asyncio.run(handle_message(selected_bot, fake_message))
                
                if result.get('success'):
                    print(f"✅ Bot: {result.get('response', 'Javob yo\'q')}")
                else:
                    print(f"❌ Xatolik: {result.get('error', 'Noma\'lum xatolik')}")
                    
            except Exception as e:
                print(f"❌ Xatolik: {str(e)}")
        
        print("\n👋 Test tugadi!")

if __name__ == '__main__':
    test_bot_locally()
