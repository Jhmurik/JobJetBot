from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

driver_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Личный кабинет")],
        [KeyboardButton(text="📢 Вакансии"), KeyboardButton(text="🌐 Сменить язык")]
    ],
    resize_keyboard=True
)
