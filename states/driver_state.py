from aiogram.fsm.state import StatesGroup, State

class DriverForm(StatesGroup):
    # 🔤 Язык интерфейса
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

    # 🚛 Рабочие предпочтения
    truck_type = State()          # Тип грузовика
    employment_type = State()     # Тип занятости (полная, временная)
    ready_to_depart = State()     # Когда готов выехать
    salary_expectation = State()  # Ожидаемая зарплата
    regions = State()             # Европа / СНГ / США (мультивыбор)

    # 📞 Контакты
    contacts = State()            # Телефон, Telegram и др.

    # ✅ Подтверждение и завершение
    confirmation = State()        # Подтверждение анкеты
    complete = State()            # Завершение
