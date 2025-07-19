from aiogram.fsm.state import StatesGroup, State

class ManagerForm(StatesGroup):
    join_code = State()
    full_name = State()
    position = State()
    phone = State()
    email = State()
    company_name = State()
    company_description = State()
    company_country = State()
    company_city = State()
    regions = State()
    confirm = State()
