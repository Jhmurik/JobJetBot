from aiogram.fsm.state import State, StatesGroup

class StartState(StatesGroup):
    language = State()
    role = State()
    regions = State()
