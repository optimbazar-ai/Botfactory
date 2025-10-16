#!/usr/bin/env python
"""
Token debug script - Bot token muammosini tekshirish
"""
import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

print(f"{Fore.CYAN}🔍 BOT TOKEN DEBUG{Style.RESET_ALL}")
print("="*50)

# Flask app va database import
try:
    from app import app, db
    from models.bot import Bot
    from models.user import User
    
    with app.app_context():
        # Barcha botlarni ko'rish
        bots = Bot.query.all()
        
        if not bots:
            print(f"{Fore.YELLOW}⚠️ Hech qanday bot topilmadi!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}📊 BOTLAR RO'YXATI:{Style.RESET_ALL}")
            print("-" * 50)
            
            for bot in bots:
                print(f"\n{Fore.CYAN}Bot ID: {bot.id}{Style.RESET_ALL}")
                print(f"  Nomi: {bot.name}")
                print(f"  Egasi: User #{bot.user_id}")
                
                if bot.telegram_token:
                    # Token mavjud
                    token_preview = f"{bot.telegram_token[:20]}..." if len(bot.telegram_token) > 20 else bot.telegram_token
                    print(f"  {Fore.GREEN}✅ Token: {token_preview}{Style.RESET_ALL}")
                    
                    if bot.telegram_username:
                        print(f"  {Fore.GREEN}✅ Username: @{bot.telegram_username}{Style.RESET_ALL}")
                    else:
                        print(f"  {Fore.YELLOW}⚠️ Username: YO'Q (token tekshirilmagan){Style.RESET_ALL}")
                else:
                    print(f"  {Fore.RED}❌ Token: YO'Q{Style.RESET_ALL}")
                    print(f"  {Fore.RED}❌ Username: YO'Q{Style.RESET_ALL}")
                
                print(f"  Yaratilgan: {bot.created_at}")
        
        # Token yangilash testi
        print(f"\n{Fore.YELLOW}📝 TOKEN YANGILASH TESTI:{Style.RESET_ALL}")
        print("-" * 50)
        
        bot_id = input("Bot ID kiriting (test uchun): ")
        if bot_id.isdigit():
            bot = Bot.query.get(int(bot_id))
            if bot:
                print(f"Bot topildi: {bot.name}")
                new_token = input("Yangi token kiriting (bo'sh = o'zgartirmaslik): ").strip()
                
                if new_token:
                    print(f"{Fore.YELLOW}⏳ Token yangilanmoqda...{Style.RESET_ALL}")
                    bot.telegram_token = new_token
                    
                    # Username olishga urinish
                    try:
                        import requests
                        response = requests.get(f'https://api.telegram.org/bot{new_token}/getMe', timeout=5)
                        if response.status_code == 200:
                            bot_info = response.json()
                            if bot_info.get('ok'):
                                bot.telegram_username = bot_info['result']['username']
                                print(f"{Fore.GREEN}✅ Bot username: @{bot.telegram_username}{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.YELLOW}⚠️ Token noto'g'ri bo'lishi mumkin{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}⚠️ Telegram API javob bermadi: {response.status_code}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.YELLOW}⚠️ Telegram API xatolik: {e}{Style.RESET_ALL}")
                    
                    # Database'ga saqlash
                    db.session.commit()
                    print(f"{Fore.GREEN}✅ Token database'ga saqlandi!{Style.RESET_ALL}")
                    
                    # Tekshirish
                    bot_check = Bot.query.get(bot.id)
                    if bot_check.telegram_token:
                        print(f"{Fore.GREEN}✅ TASDIQLANDI: Token database'da mavjud{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ XATOLIK: Token saqlanmadi!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Bot topilmadi!{Style.RESET_ALL}")
        
except ImportError as e:
    print(f"{Fore.RED}❌ Import xatolik: {e}{Style.RESET_ALL}")
    print("app.py faylida muammo bo'lishi mumkin")
except Exception as e:
    print(f"{Fore.RED}❌ Xatolik: {e}{Style.RESET_ALL}")
    import traceback
    traceback.print_exc()
