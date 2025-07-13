from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("🚛 Найти работу"),
    KeyboardButton("🏢 Я — компания")
)
main_menu.add(
    KeyboardButton("💼 Профиль"),
    KeyboardButton("⭐ Подписка Premium")
)
main_menu.add(
    KeyboardButton("🔗 Полезные сервисы"),
    KeyboardButton("❓ Помощь")
)
