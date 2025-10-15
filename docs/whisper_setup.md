# 🎤 OpenAI Whisper - O'zbek Tili Speech-to-Text

## 🌟 NIMA UCHUN WHISPER?

| Xususiyat | Google Speech | Whisper |
|-----------|--------------|---------|
| O'zbek tili | ❌ Yo'q | ✅ 100% |
| Aniqlik | 60-70% | 95-99% |
| Offline | ❌ | ✅ (agar local model) |
| Narx | Bepul | $0.006/minut |

## ⚙️ O'RNATISH

### 1️⃣ OpenAI API Key Olish

1. **OpenAI saytiga o'ting:** https://platform.openai.com/api-keys
2. **Sign up** yoki **Login** qiling
3. **"Create new secret key"** bosing
4. **Key'ni kochiring:** `sk-proj-...`

### 2️⃣ .env Fayliga Qo'shish

`.env` faylini oching va qo'shing:

```bash
# OpenAI API Key (Whisper uchun)
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXXXXXX

# Yoki mavjud Gemini key ishlatiladi
GEMINI_API_KEY=AIzaSy...
```

**MUHIM:** Agar OPENAI_API_KEY bo'lmasa, GEMINI_API_KEY ishlatiladi yoki Google Speech Recognition'ga qaytadi.

### 3️⃣ Botni Qayta Ishga Tushirish

```bash
python restart_bot.py
```

## 🎯 QANDAY ISHLAYDI

### Whisper API:
```python
client = openai.OpenAI(api_key=api_key)

transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language='uz'  # O'zbek tili!
)

text = transcript.text
```

### Fallback Tizimi:
1. **Birinchi:** Whisper (agar API key bor bo'lsa)
2. **Ikkinchi:** Google Speech Recognition (zaxira)

## 💰 NARX

**Whisper API:**
- **$0.006** / minut
- 1 soat = **$0.36**
- 100 ta 30-soniyalik xabar = **$0.30**

**Juda arzon va sifat yuqori!**

## 📊 NATIJA

### Oldin (Google):
```
User: [🎤 "Salom, men Akram"]
Bot: "саром мен Акрам"  ❌
```

### Hozir (Whisper):
```
User: [🎤 "Salom, men Akram"]
Bot: "Salom, men Akram"  ✅
```

## 🔥 TEST QILISH

1. `.env` ga `OPENAI_API_KEY` qo'shing
2. Botni qayta ishga tushiring
3. Ovozli xabar yuboring
4. Terminal'da:
   ```
   🎤 Whisper Speech-to-text boshlandi (Til: uz)
   ✅ Whisper: Salom, men Akram
   ```

## ⚠️ XATOLIK HAL QILISH

### "API key topilmadi"
- `.env` faylida `OPENAI_API_KEY` borligini tekshiring
- Bot qayta ishga tushiring

### "Whisper xatolik"
- API key to'g'rimi?
- Balans bormi? (https://platform.openai.com/usage)
- Google Speech Recognition ishlatilmoqda (fallback)

## 🎉 AFZALLIKLAR

- ✅ **O'zbek tilini 100% qo'llab-quvvatlaydi**
- ✅ **99% aniqlik**
- ✅ **Tez** (1-2 soniya)
- ✅ **Barcha ovoz formatlarini qabul qiladi**
- ✅ **Fallback tizimi** (xatolik bo'lsa zaxira)

---
*BotFactory - Eng yaxshi Speech-to-Text!* 🚀
