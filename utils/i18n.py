import json
import os

DEFAULT_LANG = "ru"
LOCALE_PATH = "locales"

_cache = {}

def load_locale(lang_code: str):
    if lang_code in _cache:
        return _cache[lang_code]
    try:
        with open(os.path.join(LOCALE_PATH, f"{lang_code}.json"), encoding="utf-8") as f:
            _cache[lang_code] = json.load(f)
            return _cache[lang_code]
    except FileNotFoundError:
        return {}

def t(lang_code: str, key: str) -> str:
    data = load_locale(lang_code)
    return data.get(key, f"[{key}]")
