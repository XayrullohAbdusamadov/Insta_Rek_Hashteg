from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.hashtags_data import CATEGORIES


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Asosiy menyu tugmalari"""
    buttons = [
        [
            InlineKeyboardButton(text="🚀 Hashtag yaratish", callback_data="start_wizard")
        ],
        [
            InlineKeyboardButton(text="💡 Rekka chiqish sirlari", callback_data="rek_tips"),
            InlineKeyboardButton(text="ℹ️ Bot haqida", callback_data="about_bot")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_categories_keyboard() -> InlineKeyboardMarkup:
    """Kategoriyalar ro'yxati tugmalari"""
    keyboard = []
    cat_items = list(CATEGORIES.items())
    
    # 2 tadan qilib joylashtirish
    for i in range(0, len(cat_items), 2):
        row = []
        cat_id1, cat_data1 = cat_items[i]
        row.append(InlineKeyboardButton(text=cat_data1["title"], callback_data=f"cat_{cat_id1}"))
        
        if i + 1 < len(cat_items):
            cat_id2, cat_data2 = cat_items[i + 1]
            row.append(InlineKeyboardButton(text=cat_data2["title"], callback_data=f"cat_{cat_id2}"))
            
        keyboard.append(row)
        
    # Maxsus so'rov va orqaga tugmalari
    keyboard.append([
        InlineKeyboardButton(text="✍️ O'z mavzuyimni yozaman", callback_data="cat_custom_input")
    ])
    keyboard.append([
        InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_size_keyboard() -> InlineKeyboardMarkup:
    """Heshteglar soni / kattaligi tugmalari"""
    buttons = [
        [
            InlineKeyboardButton(
                text="🟢 Kichik (5-8 ta) — Minimalist & Algoritm SEO",
                callback_data="size_small"
            )
        ],
        [
            InlineKeyboardButton(
                text="🟡 O'rta (15-18 ta) — Rek / Balans ⭐",
                callback_data="size_medium"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔴 Katta (25-30 ta) — Maksimal qamrov",
                callback_data="size_large"
            )
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="start_wizard")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Auditoriya tili tugmalari"""
    buttons = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha (Mahalliy rek)", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Ruscha (MDH auditoriyasi)", callback_data="lang_ru")
        ],
        [
            InlineKeyboardButton(text="🇬🇧 Inglizcha (Global rek)", callback_data="lang_en"),
            InlineKeyboardButton(text="🌐 Universal / Aralash ⭐", callback_data="lang_mix")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_size")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_post_type_keyboard() -> InlineKeyboardMarkup:
    """Format turi (Reels yoki Post)"""
    buttons = [
        [
            InlineKeyboardButton(text="🎬 Reels / Qisqa video (Rek uchun)", callback_data="type_reels"),
            InlineKeyboardButton(text="📸 Post / Karusel", callback_data="type_post")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_lang")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_result_keyboard() -> InlineKeyboardMarkup:
    """Natija sahifasidagi tugmalar"""
    buttons = [
        [
            InlineKeyboardButton(text="🔄 Boshqa variant olish", callback_data="regenerate_tags"),
            InlineKeyboardButton(text="⚙️ Almashtirish / Sozlash", callback_data="back_to_size")
        ],
        [
            InlineKeyboardButton(text="🚀 Yangi mavzu", callback_data="start_wizard"),
            InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Faqat bosh menyuga qaytish tugmasi"""
    buttons = [
        [
            InlineKeyboardButton(text="🚀 Hashtag yaratish", callback_data="start_wizard")
        ],
        [
            InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
