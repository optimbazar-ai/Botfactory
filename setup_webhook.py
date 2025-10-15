import asyncio
from app import create_app, db
from app.models.bot import Bot
from telegram import Bot as TelegramBot

async def setup_webhook(bot_id, webhook_url):
    """Setup webhook for a bot"""
    app = create_app()
    app.app_context().push()
    
    bot = Bot.query.get(bot_id)
    if not bot:
        print(f"❌ Bot #{bot_id} topilmadi!")
        return
    
    print(f"\n{'='*60}")
    print(f"🤖 Bot: {bot.name}")
    print(f"{'='*60}\n")
    
    if not bot.telegram_token:
        print("❌ Bot uchun Telegram token yo'q!")
        return
    
    try:
        telegram_bot = TelegramBot(token=bot.telegram_token)
        
        # Get bot info first
        me = await telegram_bot.get_me()
        print(f"✅ Bot topildi: @{me.username}")
        
        # Set webhook
        full_webhook_url = f"{webhook_url}/telegram/webhook/{bot_id}"
        print(f"\n🔗 Webhook o'rnatilmoqda...")
        print(f"   URL: {full_webhook_url}")
        
        result = await telegram_bot.set_webhook(url=full_webhook_url)
        
        if result:
            print(f"\n✅ Webhook muvaffaqiyatli o'rnatildi!")
            
            # Get webhook info
            webhook_info = await telegram_bot.get_webhook_info()
            print(f"\n📊 Webhook ma'lumotlari:")
            print(f"   URL: {webhook_info.url}")
            print(f"   Kutilayotgan xabarlar: {webhook_info.pending_update_count}")
            
            if webhook_info.last_error_message:
                print(f"   ⚠️ Oxirgi xato: {webhook_info.last_error_message}")
            
            print(f"\n🎉 Endi botingizga Telegramda yozishingiz mumkin!")
            print(f"   Telegram: @{me.username}")
            
        else:
            print("❌ Webhook o'rnatilmadi!")
            
    except Exception as e:
        print(f"❌ Xatolik: {str(e)}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Foydalanish: python setup_webhook.py <bot_id> <webhook_url>")
        sys.exit(1)
    
    bot_id = int(sys.argv[1])
    webhook_url = sys.argv[2]
    
    asyncio.run(setup_webhook(bot_id, webhook_url))
