from aiogram.fsm.state import StatesGroup, State

class VacancyFilter(StatesGroup):
    region = State()
    truck_type = State()
