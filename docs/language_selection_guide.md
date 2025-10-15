# 🌐 Til Tanlash - Foydalanuvchi Tili

## 🎯 Funksiya

Bot endi **har bir foydalanuvchi uchun alohida til**ni qo'llab-quvvatlaydi:
- 🇺🇿 **O'zbek tili**
- 🇷🇺 **Rus tili**
- 🇬🇧 **Ingliz tili**

## ✨ Qanday ishlaydi?

### 1️⃣ Birinchi marta /start bosganida:
```
👋 Assalomu alaykum! / Здравствуйте! / Hello!

Tilni tanlang / Выберите язык / Choose language:

[🇺🇿 O'zbek]  [🇷🇺 Русский]
      [🇬🇧 English]
```

### 2️⃣ Foydalanuvchi til tanlaydi:
- Tugmani bosadi
- Til saqlanyapti database'ga
- Xush kelibsiz xabari tanlangan tilda ko'rsatiladi

### 3️⃣ Keyingi xabarlarda:
- Bot **tanlangan tilda** javob beradi
- Audio javoblar ham **shu tilda**
- Spam xabarlari ham **shu tilda**

## 🔧 Texnik Detalllar

### Database Struktura:
```sql
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,  -- Telegram user ID
    bot_id INTEGER,   -- Bot ID
    language TEXT     -- 'uz', 'ru', 'en'
);
```

### AI Prompt:
```python
language_instructions = {
    'uz': "Javobni O'ZBEK tilida bering.",
    'ru': "Отвечайте на РУССКОМ языке.",
    'en': "Answer in ENGLISH."
}
```

## 📱 Foydalanuvchi Uchun

### Til o'zgartirish:
1. Botga qaytadan `/start` yuboring
2. Yangi til tanlang
3. Bot endi yangi tilda javob beradi

### Har bir foydalanuvchi:
- O'z tilini tanlaydi
- Til barcha sessiyalarda saqlanadi
- Boshqa foydalanuvchilarga ta'sir qilmaydi

## 🎤 Audio Javoblar

**Gemini TTS** har bir til uchun maxsus ovoz ishlatadi:

| Til | Ovoz | Tavsif |
|-----|------|---------|
| 🇺🇿 O'zbek | Kore | Ayol, yumshoq |
| 🇷🇺 Rus | Aoede | Ayol, jonli |
| 🇬🇧 Ingliz | Puck | Erkak, rasmiy |

## 🚀 Kod Misoli

### User tilini olish:
```python
user_language = self.get_user_language(user.id)
if not user_language:
    user_language = self.bot_model.language  # Default
```

### AI javob olish:
```python
ai_response = await self.get_ai_response_with_knowledge(
    message_text, 
    user_language  # User tili
)
```

### Audio yaratish:
```python
audio_file = self.text_to_speech(
    final_response, 
    user_language  # User tilida
)
```

## ✅ Afzalliklari

1. **Personalizatsiya** - har bir user o'z tilida
2. **Xalqaro** - dunyo bo'ylab foydalanish
3. **Saqlash** - til bir marta tanlanadi
4. **Audio** - har til uchun maxsus ovoz
5. **Oson** - faqat 1 marta tugma bosish

## 📊 Statistika

Database'da saqlanadi:
- Qancha user qaysi tilni tanladi
- Har bir user o'z tilini almashtirish tarixi
- Eng ko'p ishlatiladigan til

## 🔄 Kelajakdagi Rivojlantirish

- ➕ Boshqa tillar (tojik, qozoq, ...)
- 🎨 Har til uchun maxsus interfeys
- 📈 Til bo'yicha statistika
- 🤖 Avtomatik til aniqlash (xabar tilidan)

---
*BotFactory - Har bir user o'z tilida!* 🌍
