from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.i18n import t

# 📱 Главное меню для водителя
def get_driver_main_kb(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "menu_create_or_edit_profile"))],
            [KeyboardButton(text=t(lang, "menu_statistics"))],
            [KeyboardButton(text=t(lang, "menu_buy_premium"))],
            [KeyboardButton(text=t(lang, "menu_bonuses"))]
        ],
        resize_keyboard=True,
        input_field_placeholder=t(lang, "menu_placeholder")
    )

# 📱 Главное меню для менеджера
def get_manager_main_kb(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "menu_create_or_edit_company"))],
            [KeyboardButton(text=t(lang, "menu_statistics"))],
            [KeyboardButton(text=t(lang, "menu_buy_premium"))],
            [KeyboardButton(text=t(lang, "menu_bonuses"))]
        ],
        resize_keyboard=True,
        input_field_placeholder=t(lang, "menu_placeholder")
    )

# 📱 Главное меню для компании (если понадобится отдельное)
def get_company_main_kb(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "menu_statistics"))]
        ],
        resize_keyboard=True
    )
