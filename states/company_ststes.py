from aiogram.fsm.state import StatesGroup, State

class CompanyStart(StatesGroup):
    menu = State()
    name = State()
    description = State()
    country = State()
    city = State()
    join_code = State()
