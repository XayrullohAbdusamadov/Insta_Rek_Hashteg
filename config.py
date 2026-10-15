import os
import sys
from pathlib import Path

# Windows konsolida UTF-8 (emojilar) to'g'ri chiqishi uchun
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# .env fayli joylashgan asosiy papka
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"


def load_env_variables(path: Path) -> None:
    """
    .env faylidan o'zgaruvchilarni yuklash.
    Faqat Python'ning o'zida mavjud standart imkoniyatlardan foydalanadi,
    hech qanday qo'shimcha kutubxona talab qilmaydi.
    """
    if not path.is_file():
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and (key not in os.environ or not os.environ[key]):
                    os.environ[key] = val
    except Exception as e:
        print(f"Ogohlantirish (.env o'qishda): {e}")


# Muhit o'zgaruvchilarini yuklash
load_env_variables(ENV_PATH)

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
