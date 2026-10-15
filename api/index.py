import os
import json
import asyncio
from http.server import BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers.start_handler import start_router
from handlers.hashtag_wizard import wizard_router
from main import setup_bot_profile

# Aiogram Bot va Dispatcher obyektlari
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(wizard_router)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Brauzer orqali ochilganda holatni ko'rsatish va 1-bosishda webhook ulash"""
        host = self.headers.get("Host", "")
        proto = self.headers.get("X-Forwarded-Proto", "https")
        webhook_url = f"{proto}://{host}/"

        if "set_webhook" in self.path or "webhook" in self.path:
            async def set_wh():
                await setup_bot_profile(bot)
                await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
                return await bot.get_webhook_info()

            try:
                info = asyncio.run(set_wh())
                status_msg = f"✅ Telegram Webhook muvaffaqiyatli ulandi!<br><b>URL:</b> {webhook_url}<br><b>Telegram status:</b> {info.url}"
            except Exception as e:
                status_msg = f"❌ Xatolik: {e}"

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html = f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="utf-8"><title>InstaRek Bot Webhook</title></head>
            <body style="font-family: system-ui, sans-serif; text-align: center; padding: 50px; background: #0f172a; color: white;">
                <h1>🚀 InstaRek Bot Vercel Webhook</h1>
                <p style="font-size: 18px; color: #38bdf8;">{status_msg}</p>
                <br>
                <p>Endi Telegramga kirib <b>@instarek_uz_bot</b> ga <b>/start</b> yuborishingiz mumkin!</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><title>InstaRek Bot</title></head>
        <body style="font-family: system-ui, sans-serif; text-align: center; padding: 50px; background: #0f172a; color: white;">
            <h1>🚀 InstaRek Bot Vercel Serverless tizimida faol!</h1>
            <p>Webhookni ulash uchun quyidagi tugmani bosing:</p>
            <a href="/set_webhook" style="display: inline-block; padding: 12px 24px; background: #2563eb; color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">🔗 Webhookni Telegramga ulash</a>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        """Telegramdan keladigan barcha xabarlar (Webhooks) ni qabul qilish"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                update_dict = json.loads(post_data.decode('utf-8'))

                async def process():
                    update = Update.model_validate(update_dict, context={"bot": bot})
                    await dp.feed_update(bot=bot, update=update)

                asyncio.run(process())

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
