from aiogram.fsm.state import StatesGroup, State

class StartState(StatesGroup):
    language = State()
    role = State()
    region = State()
