#!/usr/bin/env python
"""
TOKEN MUAMMOSINI TUZATISH SCRIPTI
Bu script token kiritilgan lekin ko'rinmayotgan muammoni hal qiladi
"""
import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
print(f"{Fore.CYAN}🔧 TOKEN MUAMMOSINI TUZATISH{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def main():
    try:
        from app import app, db
        from models.bot import Bot
        from models.user import User
        
        with app.app_context():
            # Barcha botlarni ko'rsatish
            bots = Bot.query.all()
            
            if not bots:
                print(f"{Fore.RED}❌ Hech qanday bot topilmadi!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Avval bot yarating: /bot/create{Style.RESET_ALL}")
                return
            
            print(f"{Fore.GREEN}📊 MAVJUD BOTLAR:{Style.RESET_ALL}")
            print("-" * 40)
            
            for bot in bots:
                status = "✅ Token bor" if bot.telegram_token else "❌ Token yo'q"
                username = f"@{bot.telegram_username}" if bot.telegram_username else "Username yo'q"
                print(f"{Fore.CYAN}{bot.id}.{Style.RESET_ALL} {bot.name} - {status} - {username}")
            
            print("\n" + "-" * 60)
            
            # Bot tanlash
            bot_id = input(f"\n{Fore.YELLOW}Bot ID raqamini kiriting: {Style.RESET_ALL}").strip()
            
            if not bot_id.isdigit():
                print(f"{Fore.RED}❌ Noto'g'ri ID!{Style.RESET_ALL}")
                return
            
            bot = Bot.query.get(int(bot_id))
            if not bot:
                print(f"{Fore.RED}❌ Bot #{bot_id} topilmadi!{Style.RESET_ALL}")
                return
            
            print(f"\n{Fore.GREEN}Bot topildi: {bot.name}{Style.RESET_ALL}")
            
            # Hozirgi holatni ko'rsatish
            if bot.telegram_token:
                token_preview = bot.telegram_token[:10] + "..." + bot.telegram_token[-5:]
                print(f"Hozirgi token: {token_preview}")
                print(f"Username: @{bot.telegram_username}" if bot.telegram_username else "Username yo'q")
            else:
                print(f"{Fore.RED}Hozirda token yo'q{Style.RESET_ALL}")
            
            # Yangi token so'rash
            print(f"\n{Fore.YELLOW}@BotFather dan olingan tokenni kiriting:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Format: 123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx{Style.RESET_ALL}")
            new_token = input("Token: ").strip()
            
            if not new_token:
                print(f"{Fore.YELLOW}⚠️ Token kiritilmadi, bekor qilindi{Style.RESET_ALL}")
                return
            
            # Token formatini tekshirish
            if ':' not in new_token:
                print(f"{Fore.RED}❌ Token formati noto'g'ri! ':' belgisi yo'q{Style.RESET_ALL}")
                return
            
            # Token yangilash
            print(f"\n{Fore.YELLOW}⏳ Token yangilanmoqda...{Style.RESET_ALL}")
            bot.telegram_token = new_token
            
            # Username olishga urinish
            print(f"{Fore.YELLOW}⏳ Telegram API'dan bot ma'lumotlarini olish...{Style.RESET_ALL}")
            
            try:
                import requests
                response = requests.get(
                    f'https://api.telegram.org/bot{new_token}/getMe',
                    timeout=10
                )
                
                if response.status_code == 200:
                    bot_info = response.json()
                    if bot_info.get('ok'):
                        bot.telegram_username = bot_info['result']['username']
                        print(f"{Fore.GREEN}✅ Bot username: @{bot.telegram_username}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}✅ Bot nomi: {bot_info['result']['first_name']}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Token noto'g'ri!{Style.RESET_ALL}")
                        print(f"Xatolik: {bot_info.get('description', 'Unknown error')}")
                        confirm = input("Baribir saqlashni xohlaysizmi? (ha/yo'q): ")
                        if confirm.lower() not in ['ha', 'yes', 'y']:
                            print(f"{Fore.YELLOW}Bekor qilindi{Style.RESET_ALL}")
                            return
                else:
                    print(f"{Fore.YELLOW}⚠️ Telegram API javob bermadi: {response.status_code}{Style.RESET_ALL}")
                    print("Token baribir saqlanadi...")
                    
            except requests.exceptions.Timeout:
                print(f"{Fore.YELLOW}⚠️ Telegram API sekin ishlayapti (timeout){Style.RESET_ALL}")
                print("Token baribir saqlanadi...")
                
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Telegram API xatolik: {e}{Style.RESET_ALL}")
                print("Token baribir saqlanadi...")
            
            # Database'ga saqlash
            print(f"\n{Fore.YELLOW}💾 Database'ga saqlanmoqda...{Style.RESET_ALL}")
            db.session.commit()
            
            # Tekshirish
            bot_check = Bot.query.get(bot.id)
            if bot_check.telegram_token == new_token:
                print(f"{Fore.GREEN}✅ TOKEN MUVAFFAQIYATLI SAQLANDI!{Style.RESET_ALL}")
                
                print(f"\n{Fore.GREEN}📋 YANGILANGAN MA'LUMOTLAR:{Style.RESET_ALL}")
                print(f"  Bot ID: {bot_check.id}")
                print(f"  Bot nomi: {bot_check.name}")
                print(f"  Token: {bot_check.telegram_token[:10]}...{bot_check.telegram_token[-5:]}")
                print(f"  Username: @{bot_check.telegram_username}" if bot_check.telegram_username else "  Username: Aniqlanmadi")
                
                print(f"\n{Fore.GREEN}✨ KEYINGI QADAMLAR:{Style.RESET_ALL}")
                print("1. Sahifani yangilang (F5)")
                print("2. 'Ishga tushirish' tugmasini bosing")
                print("3. Telegram'da botingizni test qiling")
                
            else:
                print(f"{Fore.RED}❌ XATOLIK: Token saqlanmadi!{Style.RESET_ALL}")
                print("Database xatoligi bo'lishi mumkin")
                
    except ImportError as e:
        print(f"{Fore.RED}❌ Import xatolik: {e}{Style.RESET_ALL}")
        print("Kerakli kutubxonalar o'rnatilmaganmi?")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Xatolik: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    input("Chiqish uchun Enter bosing...")
