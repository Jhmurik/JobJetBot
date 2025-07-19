@router.message(Command("start"))
async def start_bot(message: Message, state: FSMContext, command: CommandObject):
    await state.clear()

    # 🔌 Подключение к базе
    app = message.bot._ctx.get("application")
    pool: Pool = app["db"]

    # 📊 Получаем статистику
    async with pool.acquire() as conn:
        drivers_count = await conn.fetchval("SELECT COUNT(*) FROM drivers")
        companies_count = await conn.fetchval("SELECT COUNT(*) FROM companies")

    stats_text = (
        f"📊 Статистика проекта JobJet AI:\n"
        f"🚚 Водителей: {drivers_count}\n"
        f"🏢 Компаний: {companies_count}\n\n"
    )

    # Deep-link
    payload = command.args
    if payload and payload.startswith("join_"):
        try:
            company_id = UUID(payload.replace("join_", ""))
            await state.update_data(join_company_id=company_id, role="manager")
        except Exception:
            await message.answer("❌ Неверный код подключения.")
            return

    await state.set_state(StartState.language)
    await message.answer(stats_text + "🌐 Пожалуйста, выберите язык:", reply_markup=get_language_keyboard())
