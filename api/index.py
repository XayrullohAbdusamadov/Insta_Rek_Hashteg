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

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(wizard_router)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Brauzer orqali ochilganda holatni ko'rsatish"""
        host = self.headers.get("Host", "instarekbot.vercel.app")
        proto = self.headers.get("X-Forwarded-Proto", "https")
        webhook_url = f"{proto}://{host}/"

        # Webhook holatini olish
        async def check():
            await setup_bot_profile(bot)
            return await bot.get_webhook_info()

        try:
            info = asyncio.run(check())
            status = f"✅ Faol (Uzluksiz ishlamoqda)"
            tg_url = info.url or webhook_url
        except Exception as e:
            status = f"Ogohlantirish: {e}"
            tg_url = webhook_url

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>InstaRek Bot — Vercel</title>
        </head>
        <body style="font-family: system-ui, -apple-system, sans-serif; text-align: center; padding: 40px 20px; background: #0b0f19; color: #f8fafc;">
            <div style="max-width: 500px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                <div style="font-size: 50px; margin-bottom: 10px;">🚀</div>
                <h2 style="color: #38bdf8; margin-top: 0;">InstaRek Bot Serverless</h2>
                <div style="background: #0f172a; padding: 15px; border-radius: 10px; text-align: left; margin: 20px 0; font-size: 14px;">
                    <p style="margin: 6px 0;"><b>Bot:</b> @instarek_uz_bot</p>
                    <p style="margin: 6px 0;"><b>Status:</b> <span style="color: #4ade80;">{status}</span></p>
                    <p style="margin: 6px 0;"><b>Webhook:</b> <code style="color: #94a3b8; font-size: 12px;">{tg_url}</code></p>
                    <p style="margin: 6px 0;"><b>Hosting:</b> Vercel 24/7</p>
                </div>
                <a href="https://t.me/instarek_uz_bot" style="display: block; padding: 14px; background: #2563eb; color: white; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 16px;">
                    🤖 Telegramda Botni Ochish
                </a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        """Telegramdan keladigan barcha yangilanishlarni qabul qilish"""
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
