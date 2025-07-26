from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🗺 Доступные регионы
REGIONS = {
    "europe": "🌍 Европа",
    "cis": "🌐 СНГ",
    "usa": "🇺🇸 США"
}

# 📦 Генератор клавиатуры выбора регионов
def get_region_keyboard(selected: list[str] = []) -> InlineKeyboardMarkup:
    keyboard = []

    for key, label in REGIONS.items():
        prefix = "✅ " if key in selected else "➖ "
        button = InlineKeyboardButton(
            text=f"{prefix}{label}",
            callback_data=f"region_toggle:{key}"
        )
        keyboard.append([button])

    # Кнопка подтверждения
    keyboard.append([
        InlineKeyboardButton(text="✅ Готово", callback_data="region_done")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# 📘 Для доступа из других файлов
__all__ = ["get_region_keyboard", "REGIONS"]
