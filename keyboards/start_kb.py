from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🌐 Выбор языка
def get_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇺🇿 Oʻzbek", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_uk")],
        [InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="lang_hi")],
        [InlineKeyboardButton(text="🇵🇱 Polski", callback_data="lang_pl")],
    ])

# 👤 Выбор роли
def get_role_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚚 Водитель", callback_data="role_driver")],
        [InlineKeyboardButton(text="🏢 Компания", callback_data="role_company")],
        [InlineKeyboardButton(text="👨‍💼 Менеджер", callback_data="role_manager")],
    ])

# 🌍 Мультивыбор регионов
def get_region_keyboard(selected: list[str] = None) -> InlineKeyboardMarkup:
    selected = selected or []
    buttons = [
        ("🇪🇺 Европа", "EU"),
        ("🌍 СНГ", "CIS"),
        ("🇺🇸 США", "USA")
    ]

    keyboard = []
    for label, code in buttons:
        is_selected = code in selected
        text = f"{'✅ ' if is_selected else ''}{label}"
        callback_data = f"region_{code}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    keyboard.append([InlineKeyboardButton(text="✅ Готово", callback_data="region_done")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
