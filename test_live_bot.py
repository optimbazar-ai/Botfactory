"""
Bot ishlayaptimi tekshirish
"""
import asyncio
from telegram import Bot

async def test_bot():
    """Bot ishlayaptimi tekshirish"""
    token = "7568964660:AAHx_cinhFhE9yo-iBmyJKjikr7iQYA8VgY"
    
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print("✅ BOT ISHLAYAPTI!")
        print(f"   Username: @{me.username}")
        print(f"   Bot nomi: {me.first_name}")
        
        # Updates tekshirish
        updates = await bot.get_updates(limit=5)
        print(f"\n📨 Oxirgi xabarlar: {len(updates)} ta")
        
        for update in updates:
            if update.message:
                print(f"   - {update.message.from_user.first_name}: {update.message.text}")
        
        print("\n🎉 BOT TO'LIQ ISHLAYAPTI!")
        print("\n📱 TELEGRAM'DA TEST QILING:")
        print(f"1. @{me.username} ga o'ting")
        print("2. /start yuboring")
        print("3. Bot javob berishi kerak!")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot())
