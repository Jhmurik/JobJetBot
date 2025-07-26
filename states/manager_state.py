from aiogram.fsm.state import StatesGroup, State

class ManagerForm(StatesGroup):
    # 👤 Личные данные менеджера
    full_name = State()
    position = State()
    phone = State()
    email = State()

    # 🏢 Компания (новая или присоединение по ID)
    company_id = State()            # Если подключение через ссылку (join_xxx)
    is_owner = State()              # True — создаёт новую фирму

    company_name = State()
    company_description = State()
    company_country = State()
    company_city = State()
    regions = State()              # Мультивыбор: Европа, СНГ, США

    # ✅ Подтверждение и завершение
    confirm = State()
    complete = State()
