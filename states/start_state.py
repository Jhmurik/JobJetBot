from aiogram.fsm.state import State, StatesGroup

class StartState(StatesGroup):
    language = State()       # 🌐 Выбор языка
    role = State()           # 👤 Выбор роли (driver | company | manager)
    regions = State()        # 🌍 Выбор регионов работы
    consent = State()        # ✅ Согласие на обработку персональных данных
