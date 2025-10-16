# 🚀 RENDER.COM ENVIRONMENT VARIABLES SOZLASH

## ✅ KERAKLI O'ZGARTIRISHLAR:

### 1️⃣ **GEMINI_API_KEY qo'shish:**

Render Dashboard → Environment Variables → **Add Variable**:

```
KEY: GEMINI_API_KEY
VALUE: AIzaSyAVAiMH4-TEuc89sd7N2ykiO_bs1Rgn_uE
```
(Sizning GOOGLE_API_KEY'ingizdan nusxa oling)

### 2️⃣ **Mavjud Variables tekshirish:**

✅ **GOOGLE_API_KEY** - Mavjud (AIzaSy...)
✅ **GEMINI_API_KEY_2** - Mavjud
✅ **DATABASE_URL** - Mavjud
✅ **FLASK_ENV** - Mavjud
✅ **SESSION_SECRET** - Mavjud
✅ **ADMIN_**** - Sozlamalar mavjud

### 3️⃣ **ADMIN_PASSWORD qo'shish:**

```
KEY: ADMIN_PASSWORD
VALUE: [xavfsiz-parol-tanlang]
```

---

## 📋 TO'LIQ SOZLAMALAR:

| Key | Value | Status |
|-----|-------|--------|
| **GEMINI_API_KEY** | AIzaSy... (GOOGLE_API_KEY'dan) | ❌ QO'SHISH KERAK |
| **ADMIN_PASSWORD** | xavfsiz-parol | ❌ QO'SHISH KERAK |
| DATABASE_URL | postgresql://... | ✅ Mavjud |
| FLASK_ENV | production | ✅ Mavjud |
| GOOGLE_API_KEY | AIzaSy... | ✅ Mavjud |
| GEMINI_API_KEY_2 | ... | ✅ Mavjud |

---

## 🎯 QADAMLAR:

1. **Render Dashboard**'ga o'ting
2. **Environment** tab'ni oching
3. **GEMINI_API_KEY** qo'shing (GOOGLE_API_KEY value'sini kochiring)
4. **ADMIN_PASSWORD** qo'shing
5. **Save Changes** bosing
6. App avtomatik qayta deploy bo'ladi (3-5 daqiqa)

---

## ✨ NATIJA:

```
✅ Bot Manager ishlaydi
✅ Gemini AI javoblar ishlaydi
✅ Admin panel ishlaydi
✅ Barcha funksiyalar faol
```

**Deploy tugagandan keyin sahifani yangilang!**
