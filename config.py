import os
from pathlib import Path
from dotenv import load_dotenv

# .env faylini yuklash
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Bot haqida ma'lumotlar
CREATOR_NAME = "Hayrulloh Abdusamadov"
BOT_NAME = "Instagram Rek Hashtag Bot"
BOT_VERSION = "2.0"

# Bot haqida to'liq matn
ABOUT_TEXT = f"""✨ <b>{BOT_NAME} v{BOT_VERSION}</b>

Ushbu bot Instagram Reels va Postlaringizni <b>rekka (Instagram tavsiyalariga)</b> olib chiqish uchun eng samarali va zamonaviy heshteglarni tanlab beradi!

👤 <b>Yaratuvchi:</b> {CREATOR_NAME}
🎯 <b>Vazifasi:</b> Instagram algoritmlariga mos (Zinapoya - Ladder strategiyasi) heshteglar to'plamini tuzish.

💡 <b>Nega bizning heshteglar rekka olib chiqadi?</b>
• Spamsiz va algoritmlar tomonidan taqiqlanmagan (White-hat)
• Mikro, o'rta va yuqori qamrovli teglarning to'g'ri balansi
• Reels tavsiyalarini faollashtiruvchi zamonaviy triggerlar
• O'zbekiston, MDH va Global auditoriyalar uchun moslangan

Savol va takliflar uchun yaratuvchi bilan bog'lanishingiz mumkin.
"""
