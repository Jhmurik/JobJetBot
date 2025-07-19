from aiogram.fsm.state import StatesGroup, State

class ManagerForm(StatesGroup):
    full_name = State()
    position = State()
    phone = State()
    email = State()
    company_name = State()
    company_country = State()
    company_city = State()
    regions = State()
    confirm = State()
