from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config import ABOUT_TEXT, CREATOR_NAME, BOT_NAME
from keyboards.inline_keyboards import get_main_menu_keyboard, get_back_to_menu_keyboard

from aiogram.exceptions import TelegramBadRequest

start_router = Router()

REK_SECRETS_TEXT = f"""🔥 <b>Instagram Reels Rekka Chiqish Sirlari (2026 Algoritmi):</b>

1️⃣ <b>Ilmoq (Hook) — Dastlabki 3 soniya:</b>
Tomoshabin videongizni davom ettirishi uchun dastlabki 3 soniyada kadrga katta, qiziqtiruvchi matn yoki kutilmagan harakat qo'ying.

2️⃣ <b>Zinapoya Heshteg Strategiyasi (Ladder):</b>
Faqat katta teglarni qo'ysangiz, videongiz bir necha soniyada pastga tushib ketadi. Bizning bot sizga mikro (10k-100k), o'rta (100k-500k) va trend teglarni to'g'ri nisbatda beradi.

3️⃣ <b>Ulashish va Saqlash (Shares & Saves):</b>
2026-yilda Instagram algoritmi eng yuqori baholaydigan ko'rsatkich — bu <i>"Ulashishlar soni" (Shares)</i>. Foydali yoki do'stlarga yuborgisi keladigan kontent qiling.

4️⃣ <b>To'g'ri Musiqa:</b>
Reels bo'limida yonida ko'tarilayotgan strelka (↗️) belgisi bo'lgan trend musiqalardan foydalaning.

5️⃣ <b>Video Sifati:</b>
Instagram sozlamalarida <i>"Eng yuqori sifatda yuklash" (Upload at highest quality)</i> funksiyasini yoqib qo'ying.

👤 <b>Yaratuvchi:</b> {CREATOR_NAME}
"""


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start buyrug'i"""
    await state.clear()
    
    user_name = message.from_user.first_name if message.from_user else "Foydalanuvchi"
    
    welcome_text = f"""Assalomu alaykum, <b>{user_name}</b>! 👋

Xush kelibsiz! Men <b>{BOT_NAME}</b>man. 🎯

Instagram Reels va postlaringizni <b>rekka (tavsiyalar lentasiga)</b> olib chiqish uchun eng samarali va zamonaviy heshteglar to'plamini tuzib beraman.

📌 <b>Bot imkoniyatlari:</b>
• Mavzuingizga mos mikro va makro teglarni tanlash
• Instagram algoritmlariga mos heshteglar hajmini belgilash
• O'zbekcha, Ruscha yoki Xalqaro auditoriyaga moslash
• Bir marta bosish orqali nusxa olish qulayligi

👤 <b>Yaratuvchi:</b> {CREATOR_NAME}

Boshlash uchun quyidagi tugmani bosing:
"""
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")


@start_router.message(Command("about"))
async def cmd_about(message: Message):
    """About buyrug'i"""
    await message.answer(ABOUT_TEXT, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")


@start_router.message(Command("tips"))
async def cmd_tips(message: Message):
    """Rekka chiqish sirlari buyrug'i"""
    await message.answer(REK_SECRETS_TEXT, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")


@start_router.callback_query(F.data == "about_bot")
async def cb_about_bot(callback: CallbackQuery):
    """Bot haqida callback"""
    await callback.answer()
    try:
        await callback.message.edit_text(ABOUT_TEXT, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        pass


@start_router.callback_query(F.data == "rek_tips")
async def cb_rek_tips(callback: CallbackQuery):
    """Rekka chiqish sirlari callback"""
    await callback.answer()
    try:
        await callback.message.edit_text(REK_SECRETS_TEXT, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        pass


@start_router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext):
    """Bosh menyuga qaytish callback"""
    await callback.answer()
    await state.clear()
    welcome_text = f"""🏠 <b>Asosiy Menyu</b>

Instagramda videolaringiz ko'proq ko'rishlar (views) va yangi obunachilar yig'ishi uchun heshteglar tayyorlashni boshlaymizmi?

👤 <b>Yaratuvchi:</b> {CREATOR_NAME}
"""
    try:
        await callback.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        pass
