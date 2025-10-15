# Telegram Bot Webhook Integration

## O'zbek tilida / На русском языке / In English

Bu qo'llanmada BotFactory ilovasiga Telegram webhook integratsiyasi haqida to'liq ma'lumot berilgan.

---

## Umumiy Ma'lumot

BotFactory endi Telegram bot'larini to'liq qo'llab-quvvatlaydi! Foydalanuvchilar Telegram orqali botlaringiz bilan suhbatlashishlari mumkin va AI (Google Gemini) javob beradi.

## Asosiy Xususiyatlar

✅ **Webhook qo'llab-quvvatlash**: Telegram dan real-time xabarlar olish  
✅ **AI javoblar**: Google Gemini bilan avtomatik javoblar  
✅ **Ko'p tillilik**: O'zbek, Rus, Ingliz tillarida ishlaydi  
✅ **Custom System Prompt**: Har bir bot o'zining system prompt ga ega  
✅ **Typing Indicator**: Javob yozilayotganda "typing..." ko'rinadi  
✅ **Xavfsizlik**: Har bir botning o'z token'i va webhook'i  

---

## Sozlash Qo'llanmasi

### 1-qadam: Telegram Bot Yarating

1. Telegram da [@BotFather](https://t.me/BotFather) ni toping
2. `/newbot` komandasini yuboring
3. Bot nomini kiriting (masalan: "My AI Assistant")
4. Username kiriting (masalan: "my_ai_assistant_bot")
5. BotFather sizga **token** beradi:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. Bu tokenni saqlang!

### 2-qadam: BotFactory da Bot Yarating

1. BotFactory ga login qiling
2. **"Create New Bot"** tugmasini bosing
3. Formani to'ldiring:
   - **Name**: Bot nomi (masalan: "Customer Support Bot")
   - **Description**: Qisqacha tavsif
   - **Language**: Til tanlang (uz/ru/en)
   - **Platform**: Telegram
   - **System Prompt**: AI ga ko'rsatma (masalan: "Sen yordamchi botsan")
   - **Telegram Token**: BotFather dan olgan tokenni kiriting
4. **"Create Bot"** tugmasini bosing

### 3-qadam: Webhook Sozlang

#### Mahalliy Test Uchun (ngrok bilan)

1. **ngrok o'rnating**:
   - [ngrok.com](https://ngrok.com/) dan yuklab oling
   - Ro'yxatdan o'ting va auth token oling

2. **Flask ilovani ishga tushiring**:
   ```bash
   python main.py
   ```

3. **Yangi terminal oching va ngrok ishga tushiring**:
   ```bash
   ngrok http 5000
   ```

4. **HTTPS URL ni nusxalang**:
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:5000
   ```

5. **BotFactory da webhook sozlang**:
   - "My Bots" ga o'ting
   - Botingizni tanlang
   - **"🔗 Webhook Setup"** tugmasini bosing
   - "Webhook Base URL" ga ngrok URL ni kiriting: `https://abc123.ngrok.io`
   - **"Set Webhook"** tugmasini bosing

#### Production Uchun

1. Ilovani serverga deploy qiling (Heroku, DigitalOcean, AWS, va h.k.)
2. HTTPS domen oling
3. Webhook Base URL ga domeningizni kiriting: `https://yourdomain.com`

### 4-qadam: Botni Sinab Ko'ring

#### Test Interface Orqali:

1. "My Bots" -> Botingiz -> **"🧪 Test Bot"**
2. Xabar yozing va "Send Test Message" ni bosing
3. AI javobini ko'ring

#### Real Telegram Orqali:

1. Telegram da botingizni toping (@your_bot_username)
2. `/start` yoki har qanday xabar yuboring
3. Bot AI javob beradi! 🎉

---

## Qanday Ishlaydi

```
[Foydalanuvchi] 
    ↓ xabar yuboradi
[Telegram Server]
    ↓ webhook orqali yuboradi
[BotFactory - /telegram/webhook/<bot_id>]
    ↓ bot ma'lumotlarini oladi
[Database - Bot Model]
    ↓ system_prompt va language
[AI Service - Google Gemini]
    ↓ javob generatsiya qiladi
[Telegram Bot API]
    ↓ javob yuboradi
[Foydalanuvchi] 
    ✅ javob oladi
```

---

## API Endpoints

### Webhook Endpoint
```
POST /telegram/webhook/<bot_id>
```
Telegram Server bu endpoint ga xabarlarni yuboradi.

**Request Body** (Telegram Update):
```json
{
  "update_id": 123456789,
  "message": {
    "message_id": 1,
    "from": {
      "id": 123456,
      "first_name": "John"
    },
    "chat": {
      "id": 123456,
      "type": "private"
    },
    "text": "Salom!"
  }
}
```

**Response**:
```json
{
  "ok": true
}
```

### Webhook Setup
```
GET/POST /telegram/setup/<bot_id>
```
Bot uchun webhook sozlash sahifasi.

### Bot Test
```
GET/POST /telegram/test/<bot_id>
```
Botni test qilish sahifasi.

---

## Xavfsizlik

### Token Xavfsizligi

⚠️ **Muhim**: Telegram tokenlarini hech qachon oshkor qilmang!

✅ **To'g'ri**:
- Token database da saqlanadi
- Faqat bot egasi ko'radi
- HTTPS orqali uzatiladi

❌ **Noto'g'ri**:
- Token ni kodga yozish
- Token ni Git'ga commit qilish
- Token ni boshqalar bilan bo'lishish

### Webhook Xavfsizligi

- Faqat HTTPS qo'llab-quvvatlanadi (HTTP ishlamaydi)
- Har bir botning o'z webhook URL'i
- Bot ID orqali authentifikatsiya

---

## Muammolarni Hal Qilish

### 1. "Webhook is not set"

**Sabab**: Webhook hali sozlanmagan  
**Yechim**:
1. "Webhook Setup" sahifasiga o'ting
2. Webhook Base URL kiriting
3. "Set Webhook" ni bosing

### 2. "Invalid token"

**Sabab**: Telegram token noto'g'ri  
**Yechim**:
1. BotFather dan yangi token oling
2. Bot sozlamalarida tokenni yangilang

### 3. "Bot not responding"

**Sabab**: Webhook URL ga ulanib bo'lmayapti  
**Yechim**:
- ngrok ishlab tuganini tekshiring
- HTTPS URL to'g'ri ekanligini tekshiring
- Flask ilova ishlab tuganini tekshiring
- Webhook Status ni tekshiring

### 4. "GOOGLE_API_KEY not set"

**Sabab**: AI API key sozlanmagan  
**Yechim**:
1. `.env` faylini oching
2. `GOOGLE_API_KEY` ni qo'shing
3. Ilovani qayta ishga tushiring

### 5. "Rate limit exceeded"

**Sabab**: Google Gemini limitga yetdi  
**Yechim**:
- Bir necha daqiqa kuting
- Premium Google AI API oling

---

## Cheklovlar

### Bepul Tarif (BotFactory)
- 1 bot maksimum
- Premium uchun yangilanish kerak

### Bepul Tarif (Google Gemini)
- 60 so'rov/daqiqa
- 1,500 so'rov/kun

### Bepul Tarif (ngrok)
- 1 ngrok jarayoni
- 40 ulanish/daqiqa
- URL har safar o'zgaradi (restart qilganda)

---

## Advanced Sozlamalar

### System Prompt Misollari

**Customer Support Bot**:
```
Sen do'stona customer support botsan. Foydalanuvchilarga 
texnik muammolarni hal qilishda yordam ber. Javoblarni 
qisqa va aniq ber. Agar javob bilmasang, "Men bu haqida 
aniq javob bera olmayman" deb ayt.
```

**Language Learning Bot**:
```
You are a language learning assistant. Help users learn 
Uzbek language. Provide translations, grammar explanations, 
and practice exercises. Always be encouraging and patient.
```

**Programming Tutor**:
```
Ты учитель программирования на Python. Объясняй концепции 
простым языком, приводи примеры кода, помогай исправлять 
ошибки. Будь терпеливым и поддерживающим.
```

### Ko'p Tillilik

Bot avtomatik ravishda foydalanuvchi tilini aniqlaydi:

```python
# O'zbek tilida
Foydalanuvchi: "Salom! Dasturlashni o'rganmoqchiman"
Bot: "Salom! Ajoyib! Qaysi dasturlash tilidan boshlamoqchisiz?..."

# Rus tilida  
Foydalanuvchi: "Привет! Помоги с Python"
Bot: "Привет! Конечно, помогу! Какой у вас вопрос по Python?..."

# Ingliz tilida
Foydalanuvchi: "Hi! Teach me coding"
Bot: "Hi! I'd love to help you learn coding! What would you like to start with?..."
```

---

## Production Deploy

### Heroku

1. **Heroku CLI o'rnating**
2. **Git repository yarating**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Heroku app yarating**:
   ```bash
   heroku create my-botfactory
   ```

4. **Environment variables sozlang**:
   ```bash
   heroku config:set SESSION_SECRET=your-secret-key
   heroku config:set GOOGLE_API_KEY=your-api-key
   ```

5. **Deploy qiling**:
   ```bash
   git push heroku main
   ```

6. **Webhook URL**:
   ```
   https://my-botfactory.herokuapp.com
   ```

### DigitalOcean / AWS / VPS

1. **Server sozlang** (Ubuntu masalan)
2. **Dependencies o'rnating**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **SSL sertifikat oling** (Let's Encrypt):
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

4. **Gunicorn bilan ishga tushiring**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```

5. **Nginx sozlang** (reverse proxy)

---

## Kod Misollari

### Telegram Service ni Ishlatish

```python
from app.services.telegram_service import (
    process_telegram_message,
    set_webhook,
    get_bot_info,
    run_async
)

# Bot ma'lumotini olish
bot_info = run_async(get_bot_info("YOUR_BOT_TOKEN"))
print(bot_info)

# Webhook sozlash
result = run_async(
    set_webhook(
        bot_token="YOUR_BOT_TOKEN",
        webhook_url="https://yourdomain.com/telegram/webhook/1"
    )
)

# Xabarni qayta ishlash
result = run_async(
    process_telegram_message(
        bot_model=bot,  # Database model
        message_text="Salom!",
        chat_id=123456
    )
)
```

---

## FAQ

**Q: Bir nechta bot yaratsa bo'ladimi?**  
A: Ha, lekin free tarif 1 bot bilan cheklangan. Premium kerak.

**Q: Bot faqat Telegram da ishlaydimi?**  
A: Hozircha ha. Keyinchalik boshqa platformalar qo'shiladi.

**Q: AI javoblar qancha vaqt oladi?**  
A: Odatda 1-3 sekund. Internet tezligiga bog'liq.

**Q: Bot offline bo'lsa nima bo'ladi?**  
A: Telegram xabarlarni saqlab turadi. Bot qayta online bo'lganda javob beradi.

**Q: Webhook URL ni qanday o'zgartiraman?**  
A: Webhook Setup sahifasida "Delete Webhook" -> yangisini sozlang.

**Q: ngrok URL har safar o'zgara turadimi?**  
A: Ha, bepul versiyada. ngrok Premium constant URL beradi.

**Q: Guruhlarda ishlaydimi?**  
A: Ha, botni guruhga qo'shing va u barcha xabarlarga javob beradi.

---

## Yordam va Qo'llab-quvvatlash

- **BotFactory Hujjatlari**: README.md, AI_INTEGRATION.md
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **python-telegram-bot**: https://docs.python-telegram-bot.org/
- **Google Gemini**: https://ai.google.dev/docs
- **ngrok**: https://ngrok.com/docs

---

## Changelog

### v1.0 - Telegram Integration
- ✅ Webhook qo'llab-quvvatlash
- ✅ AI javoblar (Google Gemini)
- ✅ Ko'p tillilik (uz/ru/en)
- ✅ System prompt qo'llab-quvvatlash
- ✅ Typing indicator
- ✅ Test interface
- ✅ Webhook management UI

### Keyingi Versiyalar
- 🔄 Suhbat tarixi
- 🔄 Inline keyboard qo'llab-quvvatlash
- 🔄 Rasm va media qo'llab-quvvatlash
- 🔄 Analytics dashboard

---

**Muvaffaqiyat! Botingiz tayyor! 🎉🤖**
