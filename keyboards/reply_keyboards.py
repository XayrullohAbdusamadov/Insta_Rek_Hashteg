from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_reply_keyboard() -> ReplyKeyboardMarkup:
    """
    Doimiy pastki menyu tugmalari (Reply Keyboard).
    Foydalanuvchi ekranning pastki qismida har doim ko'rib turadi.
    """
    buttons = [
        [
            KeyboardButton(text="🚀 Heshteg yaratish")
        ],
        [
            KeyboardButton(text="💡 Rekka chiqish sirlari"),
            KeyboardButton(text="ℹ️ Bot haqida")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Quyidagi tugmalardan birini tanlang..."
    )
