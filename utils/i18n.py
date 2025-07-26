translations = {
    "start_choose_language": {
        "ru": "🌐 Пожалуйста, выберите язык:",
        "en": "🌐 Please choose your language:",
        "uz": "🌐 Iltimos, tilni tanlang:",
        "uk": "🌐 Будь ласка, оберіть мову:",
        "hi": "🌐 कृपया अपनी भाषा चुनें:",
        "pl": "🌐 Wybierz swój język:"
    },
    "start_choose_role": {
        "ru": "👤 Кто вы?",
        "en": "👤 Who are you?",
        "uz": "👤 Siz kimsiz?",
        "uk": "👤 Хто ви?",
        "hi": "👤 आप कौन हैं?",
        "pl": "👤 Kim jesteś?"
    },
    "start_choose_region": {
        "ru": "🌍 Выберите регион(ы) для работы:",
        "en": "🌍 Select work region(s):",
        "uz": "🌍 Ishlash hudud(lar)ini tanlang:",
        "uk": "🌍 Оберіть регіон(и) для роботи:",
        "hi": "🌍 कार्य क्षेत्र चुनें:",
        "pl": "🌍 Wybierz region(y) pracy:"
    },
    "consent_text": {
        "ru": (
            "📄 Для продолжения подтвердите согласие на обработку персональных данных.\n\n"
            "Нажимая '✅ Согласен', вы даёте согласие на обработку и хранение ваших данных в рамках сервиса JobJet AI."
        ),
        "en": (
            "📄 Please confirm your consent to the processing of personal data.\n\n"
            "By clicking '✅ I Agree', you consent to the processing and storage of your data by JobJet AI."
        ),
        "uz": "📄 Davom etish uchun shaxsiy maʼlumotlarni qayta ishlashga rozilik bering.",
        "uk": "📄 Щоб продовжити, підтвердьте згоду на обробку персональних даних.",
        "hi": "📄 कृपया आगे बढ़ने के लिए व्यक्तिगत डेटा की प्रोसेसिंग के लिए सहमति दें।",
        "pl": "📄 Kontynuując, wyrażasz zgodę na przetwarzanie danych osobowych przez JobJet AI."
    },
    "consent_confirm": {
        "ru": "Пожалуйста, подтвердите:",
        "en": "Please confirm:",
        "uz": "Iltimos, tasdiqlang:",
        "uk": "Будь ласка, підтвердіть:",
        "hi": "कृपया पुष्टि करें:",
        "pl": "Proszę potwierdzić:"
    },
    "setup_complete": {
        "ru": "✅ Настройка завершена.",
        "en": "✅ Setup complete.",
        "uz": "✅ Sozlama yakunlandi.",
        "uk": "✅ Налаштування завершено.",
        "hi": "✅ सेटअप पूरा हुआ।",
        "pl": "✅ Konfiguracja zakończona."
    },
    "menu_driver": {
        "ru": "🏁 Главное меню водителя:",
        "en": "🏁 Driver main menu:",
        "uz": "🏁 Haydovchi menyusi:",
        "uk": "🏁 Меню водія:",
        "hi": "🏁 ड्राइवर मुख्य मेनू:",
        "pl": "🏁 Menu główne kierowcy:"
    },
    "menu_company": {
        "ru": "🏢 Главное меню компании:",
        "en": "🏢 Company main menu:",
        "uz": "🏢 Kompaniya menyusi:",
        "uk": "🏢 Меню компанії:",
        "hi": "🏢 कंपनी मुख्य मेनू:",
        "pl": "🏢 Menu główne firmy:"
    },
    "menu_manager": {
        "ru": "👨‍💼 Главное меню менеджера:",
        "en": "👨‍💼 Manager main menu:",
        "uz": "👨‍💼 Menedjer menyusi:",
        "uk": "👨‍💼 Меню менеджера:",
        "hi": "👨‍💼 प्रबंधक मुख्य मेनू:",
        "pl": "👨‍💼 Menu główne menedżera:"
    },
    "drivers": {
        "ru": "водителей",
        "en": "drivers",
        "uz": "haydovchilar",
        "uk": "водіїв",
        "hi": "ड्राइवर",
        "pl": "kierowców"
    },
    "companies": {
        "ru": "компаний",
        "en": "companies",
        "uz": "kompaniyalar",
        "uk": "компаній",
        "hi": "कंपनियाँ",
        "pl": "firm"
    },
    "language_changed_successfully": {
        "ru": "✅ Язык успешно обновлён!",
        "en": "✅ Language successfully changed!",
        "uz": "✅ Til muvaffaqiyatli o‘zgartirildi!",
        "uk": "✅ Мову успішно змінено!",
        "hi": "✅ भाषा सफलतापूर्वक बदल दी गई!",
        "pl": "✅ Język został pomyślnie zmieniony!"
    }
}

def t(lang: str, key: str) -> str:
    """
    Возвращает перевод строки по ключу `key` и языку `lang`.
    Если перевода нет — возвращает русский или '[missing_key]'
    """
    return translations.get(key, {}).get(lang) or translations.get(key, {}).get("ru") or f"[{key}]"
