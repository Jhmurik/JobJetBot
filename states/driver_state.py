from aiogram.fsm.state import StatesGroup, State

class DriverForm(StatesGroup):
    full_name = State()        # ФИО водителя
    birth_date = State()       # Дата рождения
    citizenship = State()      # Гражданство
    residence = State()        # Страна проживания
    license_type = State()     # Категория прав
    experience = State()       # Стаж работы
    languages = State()        # Знание языков
    documents = State()        # Наличие документов
    truck_type = State()       # Предпочтительный тип грузовика
    employment_type = State()  # Тип занятости
    ready_to_depart = State()  # Готовность к выезду
    contacts = State()         # Контактные данные
    confirmation = State()     # Подтверждение анкеты
