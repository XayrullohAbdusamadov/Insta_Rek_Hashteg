import os
import sys
import asyncio
import logging

# Windows konsolida UTF-8 (emojilar) xatosiz chiqishi uchun
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
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


async def start_render_health_server():
    """
    Render.com (va boshqa cloud hostinglar) da Free Web Service port talab qiladi.
    Agar PORT o'zgaruvchisi mavjud bo'lsa, Render tekshiruvi uchun yengil web server ochiladi.
    """
    port = os.getenv("PORT")
    if not port:
        return None

    app = web.Application()

    async def health_check(request):
        return web.Response(
            text=f"✅ {BOT_NAME} v{BOT_VERSION} faol ishlamoqda!\n👤 Yaratuvchi: {CREATOR_NAME}\n"
        )

    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(port))
    await site.start()
    logger.info(f"Render Web Service porti ({port}) muvaffaqiyatli ishga tushdi.")
    return runner


async def setup_bot_profile(bot: Bot):
    """
    Telegram bot profilini avtomatik sozlash:
    1. Yangi kirgan odam ko'radigan to'rtburchak ma'lumotlar bloki (Description)
    2. Bot haqida qisqa ma'lumot (Short Description)
    3. Telegram chap pastdagi 'Menu' tugmasi komandalari (Commands)
    """
    try:
        # Bot tavsifi (yangi kirgan foydalanuvchi ko'radigan to'rtburchak blok)
        description_text = (
            "🚀 Instagram Reels va postlaringizni REKGA (tavsiyalar lentasiga) olib chiqish uchun "
            "eng samarali va zamonaviy heshteglar boti!\n\n"
            "🎯 Imkoniyatlar:\n"
            "• Instagram 2026 Zinapoya (Ladder) algoritmi\n"
            "• 12+ ta yo'nalish yoki o'z shaxsiy mavzuingiz\n"
            "• Hajm (5-30 ta) va auditoriya tilini tanlash\n"
            "• 1 bosishda nusxa olish qulayligi\n\n"
            f"👤 Yaratuvchi: {CREATOR_NAME}\n\n"
            "Boshlash uchun pastdagi START (Boshlash) tugmasini bosing! 👇"
        )
        await bot.set_my_description(description_text)

        # Bot bio (qisqa tavsif)
        short_desc = f"Instagram Reels rek heshteglar boti. Yaratuvchi: {CREATOR_NAME}"
        await bot.set_my_short_description(short_desc)

        # Telegram menyu komandalari
        commands = [
            BotCommand(command="start", description="🏠 Bosh menyu"),
            BotCommand(command="hashtag", description="🚀 Heshteg yaratish"),
            BotCommand(command="tips", description="💡 Rekka chiqish sirlari"),
            BotCommand(command="about", description="ℹ️ Bot va Dasturchi haqida"),
        ]
        await bot.set_my_commands(commands)
        logger.info("Bot ma'lumotlari va menyu komandalari Telegramda yangilandi.")
    except Exception as e:
        logger.warning(f"Bot profilini yangilashda ogohlantirish: {e}")


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

    # Bot profilini (ekrandagi to'rtburchak ma'lumotlar va menyuni) yangilash
    await setup_bot_profile(bot)

    # Render.com uchun web server (agar PORT bo'lsa)
    web_runner = await start_render_health_server()

    print("\n" + "=" * 60)
    print(f"🚀 {BOT_NAME} v{BOT_VERSION} ishga tushdi!")
    print(f"👤 Yaratuvchi: {CREATOR_NAME}")
    print("🤖 Bot Telegramda xabarlarni kutmoqda...")
    print("=" * 60 + "\n")

    # Webhook tozalash va pollingni boshlash
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        if web_runner:
            await web_runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Bot to'xtatildi.")
