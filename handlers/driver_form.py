@router.message(DriverForm.employment_type)
async def process_employment_type(message: Message, state: FSMContext):
    await state.update_data(employment_type=message.text)
    await message.answer("Готовность к выезду (например: сегодня, через неделю и т.д.):")
    await state.set_state(DriverForm.ready_to_depart)

@router.message(DriverForm.ready_to_depart)
async def process_ready_to_depart(message: Message, state: FSMContext):
    await state.update_data(ready_to_depart=message.text)
    await message.answer("Оставьте контактные данные (номер телефона, Telegram и др.):")
    await state.set_state(DriverForm.contacts)

@router.message(DriverForm.contacts)
async def process_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)

    data = await state.get_data()
    summary = "\n".join([f"{key.replace('_', ' ').capitalize()}: {value}" for key, value in data.items()])

    await message.answer(f"Пожалуйста, проверьте анкету:\n\n{summary}\n\nПодтвердите отправку? (Да/Нет)")
    await state.set_state(DriverForm.confirmation)

@router.message(DriverForm.confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    if message.text.lower() in ["да", "подтверждаю"]:
        await message.answer("Спасибо! Ваша анкета отправлена.")
        await state.clear()
        # здесь можно добавить сохранение в БД или отправку администратору
    else:
        await message.answer("Анкета не подтверждена. Вы можете начать заново, написав 'заполнить анкету'.")
        await state.clear()
