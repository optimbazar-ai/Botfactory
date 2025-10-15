from app import create_app, db
from app.models.bot import Bot

app = create_app()
app.app_context().push()

bots = Bot.query.all()
print(f'Jami botlar: {len(bots)}')
print('-' * 60)

for bot in bots:
    token_status = "✓ Bor" if bot.telegram_token else "✗ Yoq"
    prompt_status = "✓ Bor" if bot.system_prompt else "✗ Yoq"
    active_status = "Ha" if bot.is_active else "Yoq"
    
    print(f'Bot ID: {bot.id}')
    print(f'Nomi: {bot.name}')
    print(f'Til: {bot.language}')
    print(f'Telegram Token: {token_status}')
    print(f'System Prompt: {prompt_status}')
    print(f'Faol: {active_status}')
    print(f'Knowledge Base: {bot.knowledge_bases.count()} ta fayl')
    print('-' * 60)
