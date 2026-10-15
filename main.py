import asyncio
import logging
import sys

# Windows konsolida UTF-8 (emojilar) xatosiz chiqishi uchun
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, CREATOR_NAME, BOT_NAME, BOT_VERSION
from handlers.start_handler import start_router
from handlers.hashtag_wizard import wizard_router

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "=" * 65)
        print("⚠️ DIQQAT: Bot tokeni topilmadi yoki kiritilmagan!")
        print("=" * 65)
        print("1. Telegramda @BotFather ga kiring.")
        print("2. /newbot buyrug'ini yuboring va yangi bot yarating.")
        print("3. @BotFather bergan API tokenni nusxalang.")
        print("4. Ushbu papkadagi '.env' faylini oching va quyidagicha yozing:")
        print("   BOT_TOKEN=sizning_tokeningiz")
        print("=" * 65 + "\n")
        sys.exit(1)

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(start_router)
    dp.include_router(wizard_router)

    print("\n" + "=" * 60)
    print(f"🚀 {BOT_NAME} v{BOT_VERSION} ishga tushdi!")
    print(f"👤 Yaratuvchi: {CREATOR_NAME}")
    print("🤖 Bot Telegramda xabarlarni kutmoqda...")
    print("=" * 60 + "\n")

    # Eski kutilayotgan xabarlarni o'tkazib yuborish va pollingni boshlash
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Bot to'xtatildi.")
