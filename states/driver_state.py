from aiogram.fsm.state import StatesGroup, State

class DriverForm(StatesGroup):
    full_name = State()
    birth_date = State()
    citizenship = State()
    residence = State()
    license_type = State()
    experience = State()
    languages = State()
    documents = State()
    truck_type = State()
    employment_type = State()
    ready_to_depart = State()
    contacts = State()
    confirmation = State()
