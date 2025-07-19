from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇺🇿 Oʻzbek", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_uk")],
        [InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="lang_hi")],
        [InlineKeyboardButton(text="🇵🇱 Polski", callback_data="lang_pl")],
    ])

def get_role_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚚 Водитель", callback_data="role_driver")],
        [InlineKeyboardButton(text="🏢 Компания", callback_data="role_company")],
        [InlineKeyboardButton(text="👨‍💼 Менеджер", callback_data="role_manager")],
    ])

def get_region_keyboard(selected=None):
    selected = selected or []
    buttons = [
        ("🇪🇺 Европа", "EU"),
        ("🌍 СНГ", "CIS"),
        ("🇺🇸 США", "USA")
    ]
    keyboard = [
        [InlineKeyboardButton(
            text=("✅ " if code in selected else "") + label,
            callback_data=f"region_{code}"
        )] for label, code in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="✅ Готово", callback_data="region_done")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
