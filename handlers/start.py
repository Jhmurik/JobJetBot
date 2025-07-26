from aiogram import Router, F from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton from aiogram.filters import Command, CommandObject from aiogram.fsm.context import FSMContext from states.start_state import StartState from keyboards.start_kb import get_language_keyboard, get_role_keyboard, get_region_keyboard from asyncpg import Pool from uuid import UUID

router = Router()

💬 /start (в том числе с deep-link)

@router.message(Command("start")) async def start_bot(message: Message, state: FSMContext, command: CommandObject): await state.clear()

app = message.bot._ctx.get("application")
pool: Pool = app["db"]
async with pool.acquire() as conn:
    drivers_count = await conn.fetchval("SELECT COUNT(*) FROM drivers")
    companies_count = await conn.fetchval("SELECT COUNT(*) FROM companies")

stats_text = (
    f"\U0001F4CA Статистика проекта JobJet AI:\n"
    f"\U0001F69A Водителей: {drivers_count}\n"
    f"\U0001F3E2 Компаний: {companies_count}\n\n"
)

payload = command.args
if payload and payload.startswith("join_"):
    try:
        company_id = UUID(payload.replace("join_", ""))
        await state.update_data(join_company_id=company_id, role="manager")
    except Exception:
        await message.answer("❌ Неверный код подключения.")
        return

await state.set_state(StartState.language)

start_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🟢 Старт", callback_data="start_pressed")]
])
await message.answer(stats_text + "\U0001F310 Пожалуйста, нажмите Старт:", reply_markup=start_inline_kb)

▶️ Старт после кнопки

@router.callback_query(F.data == "start_pressed") async def handle_start_button(callback: CallbackQuery, state: FSMContext): await callback.message.edit_reply_markup() await callback.message.answer("\U0001F310 Пожалуйста, выберите язык:", reply_markup=get_language_keyboard()) await state.set_state(StartState.language)

\U0001F310 Выбор языка

@router.callback_query(F.data.startswith("lang_")) async def set_language(callback: CallbackQuery, state: FSMContext): lang = callback.data.split("_")[1] await state.update_data(language=lang)

data = await state.get_data()
if data.get("role") == "manager" and data.get("join_company_id"):
    await state.update_data(regions=[])
    await state.set_state(StartState.regions)
    await callback.message.edit_text("\U0001F30D Выберите регион(ы) для работы:", reply_markup=get_region_keyboard())
else:
    await state.set_state(StartState.role)
    await callback.message.edit_text("\U0001F464 Кто вы?", reply_markup=get_role_keyboard())

\U0001F464 Выбор роли

@router.callback_query(F.data.startswith("role_")) async def set_role(callback: CallbackQuery, state: FSMContext): role = callback.data.split("_")[1] await state.update_data(role=role, regions=[]) await state.set_state(StartState.regions) await callback.message.edit_text("\U0001F30D Выберите регион(ы) для работы:", reply_markup=get_region_keyboard())

\U0001F30D Выбор региона (мультивыбор)

@router.callback_query(F.data.startswith("region_")) async def set_regions(callback: CallbackQuery, state: FSMContext): region = callback.data.split("_")[1] data = await state.get_data() regions = data.get("regions", []) role = data.get("role")

if region == "done":
    await state.update_data(regions=regions)
    await state.set_state(StartState.consent)
    await callback.message.edit_text(
        "\U0001F4C4 Для продолжения подтвердите согласие на обработку персональных данных.\n\n"
        "Нажимая '✅ Согласен', вы даёте согласие на обработку и хранение ваших данных в рамках сервиса JobJet AI."
    )
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Согласен")]],
        resize_keyboard=True
    )
    await callback.message.answer("Пожалуйста, подтвердите:", reply_markup=kb)
else:
    if region in regions:
        regions.remove(region)
    else:
        regions.append(region)
    await state.update_data(regions=regions)
    await callback.message.edit_reply_markup(reply_markup=get_region_keyboard(regions))

✅ Подтверждение согласия

@router.message(F.text == "✅ Согласен") async def confirm_consent(message: Message, state: FSMContext): data = await state.get_data() role = data.get("role") await state.update_data(consent=True)

app = message.bot._ctx.get("application")
pool: Pool = app["db"]

premium = False
if role in ["driver", "manager"]:
    async with pool.acquire() as conn:
        premium = await conn.fetchval("""
            SELECT TRUE FROM payments 
            WHERE user_id = $1 AND role = $2 AND payment_type = 'premium'
              AND created_at > (CURRENT_DATE - INTERVAL '30 days')
            LIMIT 1
        """, message.from_user.id, role) or False

await state.clear()

sub_text = "✅ Premium активен" if premium else "🔒 Без подписки"

if role == "driver":
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Создать анкету водителя")],
            [KeyboardButton(text="📄 Вакансии")],
            [KeyboardButton(text="💳 Купить подписку")],
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="🌐 Сменить язык")],
            [KeyboardButton(text="🚫 Выключить анкету")],
            [KeyboardButton(text="✅ Включить анкету (платно)")]
        ], resize_keyboard=True
    )
    await message.answer(f"✅ Настройка завершена. {sub_text}\n🏁 Главное меню:", reply_markup=kb)

elif role == "company":
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Зарегистрировать компанию")],
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="🌐 Сменить язык")]
        ], resize_keyboard=True
    )
    await message.answer("✅ Регистрация завершена.\n🏢 Главное меню компании:", reply_markup=kb)

elif role == "manager":
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨‍💼 Зарегистрироваться как менеджер")],
            [KeyboardButton(text="💳 Купить подписку")],
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="🌐 Сменить язык")]
        ], resize_keyboard=True
    )
    await message.answer(f"✅ Регистрация завершена. {sub_text}\n👨‍💼 Главное меню менеджера:", reply_markup=kb)

🌐 Смена языка из меню

@router.message(F.text == "🌐 Сменить язык") async def change_language(message: Message, state: FSMContext): await state.set_state(StartState.language) await message.answer("🌐 Пожалуйста, выберите язык:", reply_markup=get_language_keyboard())

                                                                      
