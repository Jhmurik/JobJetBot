from aiogram.fsm.state import StatesGroup, State

class DriverForm(StatesGroup):
    # 🔤 Выбор языка интерфейса
    language = State()

    # 👤 Персональные данные
    full_name = State()           # ФИО
    birth_date = State()          # Дата рождения
    citizenship = State()         # Гражданство
    residence = State()           # Текущая страна проживания

    # 🚘 Водительские данные
    license_type = State()        # Категория прав
    experience = State()          # Стаж вождения
    languages = State()           # Знание языков
    documents = State()           # Наличие документов

    # 🚛 Предпочтения по работе
    truck_type = State()          # Тип грузовика
    employment_type = State()     # Тип занятости (полная, временная)
    ready_to_depart = State()     # Когда готов к выезду

    # 📞 Контактные данные
    contacts = State()            # Телефон, Telegram и т.д.

    # ✅ Подтверждение анкеты
    confirmation = State()
