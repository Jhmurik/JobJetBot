from aiogram.fsm.state import StatesGroup, State

class VacancyForm(StatesGroup):
    title = State()
    truck_type = State()
    salary = State()
    region = State()
    requirements = State()
    contacts = State()
    confirm = State()
