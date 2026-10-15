from aiogram.fsm.state import State, StatesGroup


class HashtagWizard(StatesGroup):
    """Heshteg yaratish bosqichlari"""
    waiting_for_custom_topic = State()  # Foydalanuvchi o'z mavzusini qo'lda yozganda
    waiting_for_size = State()          # Kattaligi (Kichik, O'rta, Katta)
    waiting_for_lang = State()          # Tili (UZ, RU, EN, MIX)
    waiting_for_type = State()          # Turi (Reels yoki Post)
