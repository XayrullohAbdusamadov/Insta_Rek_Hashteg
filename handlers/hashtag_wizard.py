import os
import json
import html
import random
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from states.wizard_states import HashtagWizard
from keyboards.inline_keyboards import (
    get_categories_keyboard,
    get_size_keyboard,
    get_language_keyboard,
    get_post_type_keyboard,
    get_result_keyboard,
    get_back_to_menu_keyboard
)
from generator import generate_hashtags
from database.hashtags_data import CATEGORIES
from config import CREATOR_NAME

wizard_router = Router()

# Serverless (Vercel) va mahalliy xotira uchun kesh fayli
CUSTOM_STORAGE_FILE = Path("/tmp/user_custom_topics.json") if os.path.exists("/tmp") else Path("user_custom_topics.json")


def save_user_custom_topic(user_id: int, query: str) -> None:
    """Foydalanuvchi yozgan maxsus mavzuni saqlash"""
    try:
        data = {}
        if CUSTOM_STORAGE_FILE.exists():
            data = json.loads(CUSTOM_STORAGE_FILE.read_text(encoding="utf-8"))
        data[str(user_id)] = query
        CUSTOM_STORAGE_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def get_user_custom_topic(user_id: int) -> str:
    """Foydalanuvchi yozgan maxsus mavzuni o'qish"""
    try:
        if CUSTOM_STORAGE_FILE.exists():
            data = json.loads(CUSTOM_STORAGE_FILE.read_text(encoding="utf-8"))
            return data.get(str(user_id), "")
    except Exception:
        pass
    return ""


# 1-QADAM: Wizardni boshlash (Toifa / Mavzu tanlash)
@wizard_router.callback_query(F.data == "start_wizard")
async def start_wizard_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    text = """🎯 <b>1-Qadam: Videongiz nima haqida?</b>

Quyidagi mashhur toifalardan birini tanlang yoki o'zingiz istalgan mavzuni yozib yuboring (Masalan: <i>"novvoyxona ochish", "iphone 16 obzor", "qishloq hayoti"</i>):
"""
    try:
        await callback.message.edit_text(text, reply_markup=get_categories_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        pass


# Toifa tanlanganda
@wizard_router.callback_query(F.data.startswith("cat_") & (F.data != "cat_custom_input"))
async def category_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    cat_id = callback.data.replace("cat_", "")
    cat_title = CATEGORIES.get(cat_id, {}).get("title", cat_id)
    
    await state.update_data(category_id=cat_id, custom_query="", category_title=cat_title)
    await state.set_state(HashtagWizard.waiting_for_size)
    
    text = f"""✅ Tanlangan yo'nalish: <b>{cat_title}</b>

📏 <b>2-Qadam: Heshteglar qanday kattalikda (nechta) bo'lsin?</b>

Instagram algoritmi bo'yicha o'zingizga ma'qul hajmni tanlang:
"""
    try:
        await callback.message.edit_text(text, reply_markup=get_size_keyboard(cat_id=cat_id), parse_mode="HTML")
    except TelegramBadRequest:
        pass


# Maxsus mavzu yozish tugmasi bosilganda
@wizard_router.callback_query(F.data == "cat_custom_input")
async def ask_custom_topic(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(HashtagWizard.waiting_for_custom_topic)
    text = """✍️ <b>O'z mavzuingizni yozing:</b>

Videongiz nima haqida? Qisqacha kalit so'z yoki gap yozib yuboring:
<i>(Masalan: avtomobil ta'miri, shirinliklar tayyorlash, chet elda o'qish, shaxsiy brend...)</i>
"""
    try:
        await callback.message.edit_text(text, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        pass


# Foydalanuvchi matn yozib yuborganda
@wizard_router.message(HashtagWizard.waiting_for_custom_topic)
async def custom_topic_received(message: Message, state: FSMContext):
    user_query = message.text.strip()
    if len(user_query) < 2:
        await message.answer("Iltimos, biroz batafsilroq mavzu yoki kalit so'z yozing:")
        return

    safe_query = html.escape(user_query)
    save_user_custom_topic(message.from_user.id, user_query)
    await state.update_data(category_id="custom", custom_query=user_query, category_title=f"🎯 {safe_query}")
    await state.set_state(HashtagWizard.waiting_for_size)

    text = f"""✅ Siz kiritgan mavzu: <b>{safe_query}</b>

📏 <b>2-Qadam: Heshteglar qanday kattalikda (nechta) bo'lsin?</b>

Instagram algoritmi bo'yicha o'zingizga ma'qul hajmni tanlang:
"""
    await message.answer(text, reply_markup=get_size_keyboard(cat_id="custom"), parse_mode="HTML")


# 2-QADAM: Kattalik (Hajm) tanlanganda (Stateless: sz_{cat_id}_{size})
@wizard_router.callback_query(F.data.startswith("sz_"))
async def size_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split("_")
    cat_id = parts[1] if len(parts) > 1 else "biznes"
    size = parts[2] if len(parts) > 2 else "medium"

    await state.update_data(category_id=cat_id, size=size)
    await state.set_state(HashtagWizard.waiting_for_lang)

    size_names = {
        "small": "Kichik (5-8 ta)",
        "medium": "O'rta (15-18 ta)",
        "large": "Katta (25-30 ta)"
    }
    
    text = f"""✅ Tanlangan hajm: <b>{size_names.get(size, size)}</b>

🌐 <b>3-Qadam: Auditoriya va tili qanday bo'lsin?</b>

Videongiz qaysi hudud yoki tildagi foydalanuvchilarning tavsiyasiga (rek) chiqishi kerak?
"""
    try:
        await callback.message.edit_text(text, reply_markup=get_language_keyboard(cat_id=cat_id, size=size), parse_mode="HTML")
    except TelegramBadRequest:
        pass


# 3-QADAM: Til tanlanganda (Stateless: ln_{cat_id}_{size}_{lang})
@wizard_router.callback_query(F.data.startswith("ln_"))
async def lang_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split("_")
    cat_id = parts[1] if len(parts) > 1 else "biznes"
    size = parts[2] if len(parts) > 2 else "medium"
    lang = parts[3] if len(parts) > 3 else "mix"

    await state.update_data(category_id=cat_id, size=size, lang=lang)
    await state.set_state(HashtagWizard.waiting_for_type)

    lang_names = {
        "uz": "🇺🇿 O'zbekcha",
        "ru": "🇷🇺 Ruscha",
        "en": "🇬🇧 Inglizcha",
        "mix": "🌐 Universal / Aralash"
    }

    text = f"""✅ Tanlangan til: <b>{lang_names.get(lang, lang)}</b>

🎬 <b>4-Qadam: Video formati qanday?</b>

Reels yoki oddiy post (karusel) uchun moslashtiramiz:
"""
    try:
        await callback.message.edit_text(text, reply_markup=get_post_type_keyboard(cat_id=cat_id, size=size, lang=lang), parse_mode="HTML")
    except TelegramBadRequest:
        pass


# 4-QADAM: Format tanlanganda va GENERATSIYA (Stateless: tp_{cat_id}_{size}_{lang}_{post_type})
@wizard_router.callback_query(F.data.startswith("tp_"))
async def type_selected_and_generate(callback: CallbackQuery, state: FSMContext):
    await callback.answer("⏳ Heshteglar tayyorlanmoqda...")
    parts = callback.data.split("_")
    cat_id = parts[1] if len(parts) > 1 else "biznes"
    size = parts[2] if len(parts) > 2 else "medium"
    lang = parts[3] if len(parts) > 3 else "mix"
    post_type = parts[4] if len(parts) > 4 else "reels"

    custom_query = get_user_custom_topic(callback.from_user.id) if cat_id == "custom" else ""

    # Heshteglarni generatsiya qilish
    res = generate_hashtags(
        category_id=cat_id,
        custom_query=custom_query,
        size=size,
        lang=lang,
        post_type=post_type
    )

    size_labels = {"small": "Kichik", "medium": "O'rta (Rek)", "large": "Katta"}
    lang_labels = {"uz": "O'zbekcha", "ru": "Ruscha", "en": "Inglizcha", "mix": "Universal"}
    type_labels = {"reels": "🎬 Reels", "post": "📸 Post / Karusel"}

    cat_title = html.escape(str(res['category_title']))

    result_text = f"""🎉 <b>Heshteglar tayyor! Videongiz rekka chiqishiga tilakdoshmiz!</b> 🚀

📌 <b>Toifa:</b> {cat_title}
📏 <b>Hajmi:</b> {res['count']} ta ({size_labels.get(size, size)})
🌐 <b>Auditoriya:</b> {lang_labels.get(lang, lang)}
🎬 <b>Format:</b> {type_labels.get(post_type, post_type)}

📋 <b>Nusxa olish uchun pastdagi matn ustiga 1 marta bosing:</b>
<code>{res['tags_string']}</code>

💡 <b>Maslahat:</b>
Ushbu heshteglarni Reels tavsifi (caption) oxiriga yoki birinchi izohga (comment) joylang.
Videoni eng qizg'in vaqtlarda (18:00 - 21:00) yuklash tavsiya etiladi!

👤 <b>Yaratuvchi:</b> {CREATOR_NAME}
"""
    try:
        await callback.message.edit_text(
            result_text,
            reply_markup=get_result_keyboard(cat_id=cat_id, size=size, lang=lang, post_type=post_type),
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        pass


# Qayta generatsiya qilish (Boshqa variant olish: rg_{cat_id}_{size}_{lang}_{post_type})
@wizard_router.callback_query(F.data.startswith("rg_"))
async def regenerate_tags_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("🔄 Yangi variant tuzilmoqda...")
    parts = callback.data.split("_")
    cat_id = parts[1] if len(parts) > 1 else "biznes"
    size = parts[2] if len(parts) > 2 else "medium"
    lang = parts[3] if len(parts) > 3 else "mix"
    post_type = parts[4] if len(parts) > 4 else "reels"

    custom_query = get_user_custom_topic(callback.from_user.id) if cat_id == "custom" else ""

    res = generate_hashtags(
        category_id=cat_id,
        custom_query=custom_query,
        size=size,
        lang=lang,
        post_type=post_type
    )

    size_labels = {"small": "Kichik", "medium": "O'rta (Rek)", "large": "Katta"}
    lang_labels = {"uz": "O'zbekcha", "ru": "Ruscha", "en": "Inglizcha", "mix": "Universal"}
    type_labels = {"reels": "🎬 Reels", "post": "📸 Post / Karusel"}

    cat_title = html.escape(str(res['category_title']))
    rand_badge = random.randint(10, 99)

    result_text = f"""🔄 <b>Yangi variant #{rand_badge} tayyorlandi!</b> 🚀

📌 <b>Toifa:</b> {cat_title}
📏 <b>Hajmi:</b> {res['count']} ta ({size_labels.get(size, size)})
🌐 <b>Auditoriya:</b> {lang_labels.get(lang, lang)}
🎬 <b>Format:</b> {type_labels.get(post_type, post_type)}

📋 <b>Nusxa olish uchun pastdagi matn ustiga 1 marta bosing:</b>
<code>{res['tags_string']}</code>

💡 <b>Maslahat:</b>
Har bir videongizga bir xil teglarni takrorlayvermasdan, turli variantlardan foydalaning. Bu Instagram tomonidan spam deb hisoblanishining oldini oladi.

👤 <b>Yaratuvchi:</b> {CREATOR_NAME}
"""
    try:
        await callback.message.edit_text(
            result_text,
            reply_markup=get_result_keyboard(cat_id=cat_id, size=size, lang=lang, post_type=post_type),
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        pass
