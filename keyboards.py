from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/driver")],
        [KeyboardButton(text="/company")]
    ],
    resize_keyboard=True
)
