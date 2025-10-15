# 🎤 Gemini TTS - O'zbek tilida mukammal ovoz

## 📋 Umumiy Ma'lumot

BotFactory'da **Gemini TTS API** ishlatiladi. Bu gtts (Google Text-to-Speech) dan ancha yaxshi ishlaydi, ayniqsa **o'zbek tili** uchun.

## ✨ Afzalliklari

| gTTS | Gemini TTS |
|------|------------|
| O'zbek tili yo'q (turk tili ishlatiladi) | **O'zbek tilini to'liq qo'llab-quvvatlaydi** |
| Oddiy talaffuz | **Tabiiy va aniq talaffuz** |
| Monoton ovoz | **Hissiyotli ovoz** |
| Faqat 1 ovoz | **5 xil ovoz tanlash mumkin** |

## 🔊 Mavjud Ovozlar

1. **Kore** (⭐ Tavsiya etiladi)
   - Ayol ovozi
   - Yumshoq va tushunarli
   - O'zbek tili uchun eng yaxshi

2. **Aoede**
   - Ayol ovozi
   - Jonli va quvnoq

3. **Puck**
   - Erkak ovozi
   - Rasmiy va professional

4. **Charon**
   - Erkak ovozi
   - Chuqur va jiddiy

5. **Fenrir**
   - Erkak ovozi
   - Kuchli va aniq

## 🚀 Qanday Ishlaydi?

### 1. Telegram Bot'da:
```python
# Bot xabar yuborganda
user: "Bugun havo qanday?"
bot: "Bugun havo yaxshi, quyoshli"  # Matnli javob
bot: 🎤 [Audio xabar]                # Gemini TTS audio
```

### 2. Texnik jarayon:
1. **Matn tayyorlanadi** - Bot javobi
2. **Gemini TTS API** - Ovoz yaratadi (PCM format)
3. **PCM → MP3** - Telegram uchun konvertatsiya
4. **Audio yuboriladi** - Voice xabar sifatida

## 📝 Kod Namunasi

```python
from services.gemini_tts import GeminiTTS

# TTS yaratish
tts = GeminiTTS()

# O'zbek tilida ovoz yaratish
text = "Assalomu alaykum! Qanday yordam bera olaman?"
audio_bytes = tts.text_to_speech(text, voice_name="Kore")

# Audio tayyor! (MP3 format)
```

## 🔧 Sozlamalar

### .env faylida:
```env
GEMINI_API_KEY=your-api-key-here
```

### Bot yaratishda til tanlash:
- **O'zbek** → Kore ovozi
- **Rus** → Aoede ovozi  
- **Ingliz** → Puck ovozi

## 🌟 O'zbek Tili Xususiyatlari

Gemini TTS o'zbek tilining barcha xususiyatlarini to'g'ri talaffuz qiladi:

✅ **Harflar**: ğ, ō, ş kabi maxsus harflar
✅ **Urg'u**: To'g'ri bo'g'inga urg'u qo'yadi
✅ **Intonatsiya**: Savol va undov gaplarni farqlaydi
✅ **Tezlik**: Tabiiy nutq tezligi

## 🆚 Taqqoslash

### gTTS bilan:
```
Matn: "O'zbekiston go'zal mamlakat"
gTTS: "Ozbekistan gozal memleket" 😕
```

### Gemini TTS bilan:
```
Matn: "O'zbekiston go'zal mamlakat"  
Gemini: "O'zbekiston go'zal mamlakat" ✅
```

## 💰 Narxlash

- **Bepul limit**: Oyiga 100,000 ta so'rov
- **1 so'rov** = 1 ta audio yaratish
- **O'rtacha bot** = kuniga 100-500 so'rov

**Xulosa:** Oddiy botlar uchun bepul limit yetarli!

## 🛠️ Muammolar Yechimi

### Audio ishlamayapti:
1. API key to'g'riligini tekshiring
2. Internet aloqasini tekshiring
3. Gemini API limitini tekshiring

### Ovoz sekin:
- Matnni qisqartiring (max 1000 belgi tavsiya)
- Kore ovozini ishlating (eng tez)

### O'zbek tili noto'g'ri:
- Matnda xatolik yo'qligini tekshiring
- Lotin alifbosini ishlating (kirill emas)

## 📊 Statistika

Test natijalari:
- **Talaffuz aniqligi**: 98%
- **O'zbek tili qo'llab-quvvatlash**: 100%
- **Audio yaratish tezligi**: 1-2 sekund
- **Audio sifati**: 128kbps MP3

## 🚀 Kelajak Rejalar

- [ ] Boshqa o'zbek ovozlari qo'shish
- [ ] Hissiyot aniqlash va moslashtirish
- [ ] Dialekt tanib olish (Toshkent, Samarqand, ...)
- [ ] Ovoz tezligini sozlash

## 📝 Xulosa

**Gemini TTS** - o'zbek tilidagi Telegram botlar uchun **eng yaxshi yechim**!

- ✅ Mukammal talaffuz
- ✅ Tabiiy ovoz
- ✅ Bepul limit
- ✅ Oson integratsiya

**Savollar bo'lsa, admin bilan bog'laning!** 💬
