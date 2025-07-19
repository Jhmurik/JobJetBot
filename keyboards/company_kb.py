from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_company_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏢 Зарегистрировать компанию", callback_data="company_register")],
        [InlineKeyboardButton(text="🔑 Подключиться как менеджер", callback_data="company_join")]
    ])
