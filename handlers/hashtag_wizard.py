from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

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


# 1-QADAM: Wizardni boshlash (Toifa / Mavzu tanlash)
@wizard_router.callback_query(F.data == "start_wizard")
async def start_wizard_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = """🎯 <b>1-Qadam: Videongiz nima haqida?</b>

Quyidagi mashhur toifalardan birini tanlang yoki o'zingiz istalgan mavzuni yozib yuboring (Masalan: <i>"novvoyxona ochish", "iphone 16 obzor", "qishloq hayoti"</i>):
"""
    await callback.message.edit_text(text, reply_markup=get_categories_keyboard(), parse_mode="HTML")
    await callback.answer()


# Toifa tanlanganda
@wizard_router.callback_query(F.data.startswith("cat_") & (F.data != "cat_custom_input"))
async def category_selected(callback: CallbackQuery, state: FSMContext):
    cat_id = callback.data.replace("cat_", "")
    cat_title = CATEGORIES.get(cat_id, {}).get("title", cat_id)
    
    await state.update_data(category_id=cat_id, custom_query="", category_title=cat_title)
    await state.set_state(HashtagWizard.waiting_for_size)
    
    text = f"""✅ Tanlangan yo'nalish: <b>{cat_title}</b>

📏 <b>2-Qadam: Heshteglar qanday kattalikda (nechta) bo'lsin?</b>

Instagram algoritmi bo'yicha o'zingizga ma'qul hajmni tanlang:
"""
    await callback.message.edit_text(text, reply_markup=get_size_keyboard(), parse_mode="HTML")
    await callback.answer()


# Maxsus mavzu yozish tugmasi bosilganda
@wizard_router.callback_query(F.data == "cat_custom_input")
async def ask_custom_topic(callback: CallbackQuery, state: FSMContext):
    await state.set_state(HashtagWizard.waiting_for_custom_topic)
    text = """✍️ <b>O'z mavzuingizni yozing:</b>

Videongiz nima haqida? Qisqacha kalit so'z yoki gap yozib yuboring:
<i>(Masalan: avtomobil ta'miri, shirinliklar tayyorlash, chet elda o'qish, shaxsiy brend...)</i>
"""
    await callback.message.edit_text(text, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")
    await callback.answer()


# Foydalanuvchi matn yozib yuborganda
@wizard_router.message(HashtagWizard.waiting_for_custom_topic)
async def custom_topic_received(message: Message, state: FSMContext):
    user_query = message.text.strip()
    if len(user_query) < 2:
        await message.answer("Iltimos, biroz batafsilroq mavzu yoki kalit so'z yozing:")
        return

    await state.update_data(category_id="custom", custom_query=user_query, category_title=f"🎯 {user_query}")
    await state.set_state(HashtagWizard.waiting_for_size)

    text = f"""✅ Siz kiritgan mavzu: <b>{user_query}</b>

📏 <b>2-Qadam: Heshteglar qanday kattalikda (nechta) bo'lsin?</b>

Instagram algoritmi bo'yicha o'zingizga ma'qul hajmni tanlang:
"""
    await message.answer(text, reply_markup=get_size_keyboard(), parse_mode="HTML")


# 2-QADAM: Kattalik (Hajm) tanlanganda
@wizard_router.callback_query(F.data.startswith("size_"))
async def size_selected(callback: CallbackQuery, state: FSMContext):
    size = callback.data.replace("size_", "")
    await state.update_data(size=size)
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
    await callback.message.edit_text(text, reply_markup=get_language_keyboard(), parse_mode="HTML")
    await callback.answer()


# Orqaga: Kattalikni tanlashga qaytish
@wizard_router.callback_query(F.data == "back_to_size")
async def back_to_size_step(callback: CallbackQuery, state: FSMContext):
    await state.set_state(HashtagWizard.waiting_for_size)
    text = """📏 <b>2-Qadam: Heshteglar qanday kattalikda bo'lsin?</b>

Quyidagi variantlardan birini tanlang:
"""
    await callback.message.edit_text(text, reply_markup=get_size_keyboard(), parse_mode="HTML")
    await callback.answer()


# 3-QADAM: Til tanlanganda
@wizard_router.callback_query(F.data.startswith("lang_"))
async def lang_selected(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.replace("lang_", "")
    await state.update_data(lang=lang)
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
    await callback.message.edit_text(text, reply_markup=get_post_type_keyboard(), parse_mode="HTML")
    await callback.answer()


# Orqaga: Til tanlashga qaytish
@wizard_router.callback_query(F.data == "back_to_lang")
async def back_to_lang_step(callback: CallbackQuery, state: FSMContext):
    await state.set_state(HashtagWizard.waiting_for_lang)
    text = """🌐 <b>3-Qadam: Auditoriya va tili qanday bo'lsin?</b>

Quyidagi variantlardan birini tanlang:
"""
    await callback.message.edit_text(text, reply_markup=get_language_keyboard(), parse_mode="HTML")
    await callback.answer()


# 4-QADAM: Format tanlanganda va GENERATSIYA
@wizard_router.callback_query(F.data.startswith("type_"))
async def type_selected_and_generate(callback: CallbackQuery, state: FSMContext):
    post_type = callback.data.replace("type_", "")
    await state.update_data(post_type=post_type)
    
    data = await state.get_data()
    
    category_id = data.get("category_id", "custom")
    custom_query = data.get("custom_query", "")
    size = data.get("size", "medium")
    lang = data.get("lang", "mix")

    # Heshteglarni generatsiya qilish
    res = generate_hashtags(
        category_id=category_id,
        custom_query=custom_query,
        size=size,
        lang=lang,
        post_type=post_type
    )

    size_labels = {"small": "Kichik", "medium": "O'rta (Rek)", "large": "Katta"}
    lang_labels = {"uz": "O'zbekcha", "ru": "Ruscha", "en": "Inglizcha", "mix": "Universal"}
    type_labels = {"reels": "🎬 Reels", "post": "📸 Post / Karusel"}

    result_text = f"""🎉 <b>Heshteglar tayyor! Videongiz rekka chiqishiga tilakdoshmiz!</b> 🚀

📌 <b>Toifa:</b> {res['category_title']}
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
    await callback.message.edit_text(result_text, reply_markup=get_result_keyboard(), parse_mode="HTML")
    await callback.answer("✅ Heshteglar muvaffaqiyatli tayyorlandi!")


# Qayta generatsiya qilish (Boshqa variant olish)
@wizard_router.callback_query(F.data == "regenerate_tags")
async def regenerate_tags_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        await callback.answer("Iltimos, qaytadan boshlang.", show_alert=True)
        return

    category_id = data.get("category_id", "custom")
    custom_query = data.get("custom_query", "")
    size = data.get("size", "medium")
    lang = data.get("lang", "mix")
    post_type = data.get("post_type", "reels")

    res = generate_hashtags(
        category_id=category_id,
        custom_query=custom_query,
        size=size,
        lang=lang,
        post_type=post_type
    )

    size_labels = {"small": "Kichik", "medium": "O'rta (Rek)", "large": "Katta"}
    lang_labels = {"uz": "O'zbekcha", "ru": "Ruscha", "en": "Inglizcha", "mix": "Universal"}
    type_labels = {"reels": "🎬 Reels", "post": "📸 Post / Karusel"}

    result_text = f"""🔄 <b>Yangi variant tayyorlandi!</b> 🚀

📌 <b>Toifa:</b> {res['category_title']}
📏 <b>Hajmi:</b> {res['count']} ta ({size_labels.get(size, size)})
🌐 <b>Auditoriya:</b> {lang_labels.get(lang, lang)}
🎬 <b>Format:</b> {type_labels.get(post_type, post_type)}

📋 <b>Nusxa olish uchun pastdagi matn ustiga 1 marta bosing:</b>
<code>{res['tags_string']}</code>

💡 <b>Maslahat:</b>
Har bir videongizga bir xil teglarni takrorlayvermasdan, turli variantlardan foydalaning. Bu Instagram tomonidan spam deb hisoblanishining oldini oladi.

👤 <b>Yaratuvchi:</b> {CREATOR_NAME}
"""
    await callback.message.edit_text(result_text, reply_markup=get_result_keyboard(), parse_mode="HTML")
    await callback.answer("🔄 Yangi variant tuzildi!")
