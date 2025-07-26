# utils/locales.py

LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "uz": "🇺🇿 Oʻzbek",
    "uk": "🇺🇦 Українська",
    "hi": "🇮🇳 हिन्दी",
    "pl": "🇵🇱 Polski"
}

DEFAULT_LANGUAGE = "ru"

def get_language_name(code: str) -> str:
    return LANGUAGES.get(code, "Unknown")

def get_default_language() -> str:
    return DEFAULT_LANGUAGE
