from aiogram.fsm.state import StatesGroup, State

class VacancyForm(StatesGroup):
    title = State()           # Заголовок вакансии
    truck_type = State()      # Тип грузовика
    salary = State()          # Зарплата
    region = State()          # Регион работы
    requirements = State()    # Требования
    contacts = State()        # Контакты для связи
    confirm = State()         # Подтверждение публикации
