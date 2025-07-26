import json
import os

# 📄 Файл с переводами (если используешь внешнюю структуру — например JSON)
I18N_FILE = os.path.join(os.path.dirname(__file__), "i18n_strings.json")

try:
    with open(I18N_FILE, "r", encoding="utf-8") as f:
        translations = json.load(f)
except Exception as e:
    print(f"❌ Ошибка загрузки переводов: {e}")
    translations = {}

def t(lang: str, key: str, **kwargs) -> str:
    """
    Получает перевод по ключу и языку.
    Если не найден — fallback на русский или [ключ].
    Поддерживает подстановки через format.
    """
    text = translations.get(key, {}).get(lang) \
        or translations.get(key, {}).get("ru") \
        or f"[{key}]"
    return text.format(**kwargs)
