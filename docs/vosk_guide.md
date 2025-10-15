# 🎤 VOSK - BEPUL OFFLINE SPEECH RECOGNITION

## 🎯 NIMA UCHUN VOSK?

| Xususiyat | Google Speech | Whisper | VOSK |
|-----------|--------------|---------|------|
| O'zbek tili | ❌ Yo'q | ✅ Ha | ✅ Ha |
| Aniqlik | 60-70% | 99% | 85-95% |
| Narx | Bepul | $0.006/min | **BEPUL** |
| Internet | ✅ Kerak | ✅ Kerak | ❌ **Offline** |
| Model hajmi | - | - | 45 MB |

## ✅ AFZALLIKLARI

- ✅ **100% BEPUL** - hech qanday to'lov yo'q
- ✅ **OFFLINE** - internet kerak emas
- ✅ **O'zbek tilini qo'llab-quvvatlaydi** - maxsus model
- ✅ **Tez** - 1-2 soniya
- ✅ **Xavfsiz** - ma'lumot serverga yuborilmaydi

## 📦 O'RNATISH

### 1️⃣ Kutubxonani o'rnatish:

```bash
pip install vosk
```

### 2️⃣ Modelni yuklab olish:

```bash
python download_vosk_model.py
```

**Model:**
- O'zbek tili: `vosk-model-small-uz-0.22`
- Hajm: ~45 MB
- Offline ishlaydi

### 3️⃣ Tayyor!

Bot avtomatik VOSK ishlatadi.

## 🎯 QANDAY ISHLAYDI

### Jarayon:

1. **Telegram OGG** → WAV (16kHz, mono)
2. **VOSK model** → matnni tanib oladi
3. **Natija** → bot javob beradi

### Terminal log:

```
🎤 VOSK Speech-to-text boshlandi (Til: uz)
📦 Model yuklanmoqda...
✅ VOSK (BEPUL): assalomu alaykum qalaysiz
```

## 💡 TEST QILISH

1. Telegram'da botga `/uz` yuboring
2. Ovozli xabar yuboring: "Assalomu alaykum"
3. Bot javob beradi:
   - 📝 Siz aytdingiz: assalomu alaykum
   - Matn javobi
   - 🎤 Audio javobi

## 📊 NATIJA

### O'zbek tilida:
```
User: [🎤 "Salom, men Akram"]
VOSK: "salom men akram"  ✅
```

### Rus tilida:
```
User: [🎤 "Привет, как дела?"]
VOSK: "привет как дела"  ✅
```

**DIQQAT:** VOSK kichik harfda qaytaradi.

## ⚙️ SOZLAMALAR

### Modellar:

- **Small** (45 MB) - tez, 85-90% aniqlik
- **Large** (1.8 GB) - sekin, 95-99% aniqlik

Bizda: `vosk-model-small-uz-0.22` (tavsiya)

### Tillar:

- O'zbek (uz)
- Rus (ru)
- Ingliz (en)
- 20+ boshqa tillar

## ⚠️ XATOLIK HAL QILISH

### "Model topilmadi"

```bash
python download_vosk_model.py
```

### "VOSK matn tanimadi"

- Ovozli xabar juda qisqa bo'lishi mumkin
- Shovqin ko'p bo'lishi mumkin
- Aniq gapiring

### Model yangilash

```bash
# Eski modelni o'chirish
rm -rf models/vosk-model-small-uz-0.22

# Yangi modelni yuklab olish
python download_vosk_model.py
```

## 🚀 XULOSA

**VOSK - ENG YAXSHI BEPUL VARIANT:**

- ✅ Pul to'lamang
- ✅ Internet kerak emas
- ✅ O'zbek tilini yaxshi taniydi
- ✅ Xavfsiz va tez

**Pullik Whisper dan farqi:**
- Whisper: 99% aniqlik, $0.006/minut
- VOSK: 85-95% aniqlik, **BEPUL**

**85-95% aniqlik ko'p hollarda yetarli!**

---
*BotFactory - Bepul va offline speech recognition!* 🎉
