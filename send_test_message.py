"""
Botga test xabar yuborish
"""
import asyncio
from telegram import Bot

async def send_test():
    """Test xabar yuborish"""
    token = "7568964660:AAHx_cinhFhE9yo-iBmyJKjikr7iQYA8VgY"
    chat_id = "1021369075"  # Admin chat ID
    
    try:
        bot = Bot(token=token)
        
        # 1. /uz komandasi yuborish
        print("1️⃣ /uz komandasi yuborish...")
        await bot.send_message(chat_id=chat_id, text="/uz")
        await asyncio.sleep(2)
        
        # 2. Test xabar yuborish
        print("2️⃣ Test xabar yuborish...")
        await bot.send_message(chat_id=chat_id, text="Salom, qalaysiz?")
        await asyncio.sleep(2)
        
        # 3. Updates olish
        print("3️⃣ Bot javobini tekshirish...")
        updates = await bot.get_updates(limit=10)
        
        print(f"\n✅ Test muvaffaqiyatli!")
        print(f"Oxirgi {len(updates)} ta xabar:")
        for update in updates[-5:]:
            if update.message:
                print(f"   - {update.message.text}")
        
        print("\n📱 Telegram'da bot javobini tekshiring!")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == "__main__":
    asyncio.run(send_test())
