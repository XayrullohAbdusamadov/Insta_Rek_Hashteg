# 🚀 Instagram Rek Hashtag Telegram Bot

Instagram Reels va postlarni **rekka (Instagram tavsiyalar lentasiga)** olib chiqish uchun professional heshteg generator boti.

👤 **Yaratuvchi:** Hayrulloh Abdusamadov  
⚡ **Dasturlash tili:** Python 3.12 (aiogram 3.x)

---

## 🌟 Botning Asosiy Imkoniyatlari

1. **Instagram 2026 Algoritmi (Zinapoya - Ladder Strategiyasi):**
   - 🎯 **Niche (Mikro-teglar 10k-100k):** Videongizning aniq mavzusi (raqobat kam, tez ko'tariladi).
   - 👥 **Audience (O'rta-teglar 100k-500k):** Tomoshabinlar va hamjamiyat teglari.
   - 🌐 **General (Katta qamrov 500k-2M):** Keng qamrovli teglar.
   - ⚡ **Rek Triggers:** Instagram tavsiyalar tizimiga signal beruvchi zamonaviy teglar (`#reelsuzb`, `#trenduz`, `#rekkachiq`, `#reelsinstagram` va b.).

2. **Foydalanuvchidan so'raladigan parametrlar (Wizard):**
   - **Mavzu:** 12+ ta tayyor toifalar (Biznes, Avto, Motivatsiya, IT, Retsept, Sport, Yumor...) yoki foydalanuvchi yozgan ixtiyoriy matn.
   - **Kattalik (Hajmi):**
     - 🟢 *Kichik (5-8 ta)* — Minimalist & Algoritm SEO (Instagram tavsiyasi)
     - 🟡 *O'rta (15-18 ta)* — Oltin oraliq / Rek (Tavsiya etiladi ⭐)
     - 🔴 *Katta (25-30 ta)* — Maksimal qamrov
   - **Auditoriya / Tili:** 🇺🇿 O'zbekcha, 🇷🇺 Ruscha, 🇬🇧 Inglizcha, 🌐 Universal (Aralash).
   - **Formati:** 🎬 Reels / Qisqa video yoki 📸 Post / Karusel.

3. **Bir bosishda nusxalash (One-tap Copy):**
   - Natijalar `<code>#tag1 #tag2...</code>` shaklida chiqadi. Ustiga bitta bosish orqali matn buferga (clipboard) olinadi.
   - 🔄 *Boshqa variant olish* tugmasi orqali shu parametrlarda yangi kombinatsiya olish mumkin.

4. **Bot haqida bo'limi:**
   - Botga kirganda va `/about` buyrug'ida:
   - `👤 Yaratuvchi: Hayrulloh Abdusamadov` aniq ko'rsatilgan.

---

## 🛠 Ishga Tushirish Yo'riqnomasi

### 1-Qadam: Bot Tokenini Olish
1. Telegramda [@BotFather](https://t.me/BotFather) botiga kiring.
2. `/newbot` buyrug'ini yuboring.
3. Botingizga nom va username bering.
4. `@BotFather` bergan API tokenni nusxalab oling.

### 2-Qadam: Tokenni `.env` fayliga yozish
Papkadagi `.env` faylini oching va tokenni yozing:
```env
BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ
```

### 3-Qadam: Botni Ishga Tushirish

**Windows foydalanuvchilari uchun:**
Papkadagi `start_bot.bat` faylini 2 marta bosing! Bot avtomatik ishga tushadi.

Yoki terminal orqali:
```bash
python main.py
```

---

## 📂 Fayllar Strukturasi

```
kanal_uchun/
│
├── config.py                  # Bot sozlamalari va Yaratuvchi ma'lumotlari
├── generator.py               # Algoritm asosida heshteg tuzish mexanizmi
├── main.py                    # Botni ishga tushiruvchi asosiy fayl
├── start_bot.bat              # Windows uchun bir tugmali ishga tushiruvchi
├── requirements.txt           # Kutubxonalar ro'yxati (aiogram, python-dotenv)
├── .env                       # Bot tokeni
├── .env.example               # Token namunasi
│
├── database/
│   └── hashtags_data.py       # Boyitilgan nishalar, kalit so'zlar va rek triggerlari
│
├── handlers/
│   ├── start_handler.py       # /start, /about, /tips, menyu handlerlari
│   └── hashtag_wizard.py      # Bosqichma-bosqich so'rovlar (FSM wizard)
│
├── keyboards/
│   └── inline_keyboards.py    # Chiroyli inline tugmalar
│
└── states/
    └── wizard_states.py       # FSM holatlari
```

---
*Yaratuvchi: Hayrulloh Abdusamadov*
