from aiogram import Router, types
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "driver_subscription_info")
async def show_driver_subscription(callback: CallbackQuery):
    await callback.answer()

    text = (
        "💳 *Подписка для водителей:*\n\n"
        "🔓 *Бесплатно:*\n"
        "• Создание анкеты\n"
        "• Просмотр вакансий\n"
        "• Общая статистика\n\n"
        "⭐️ *Premium — $3/мес или $32/год:*\n"
        "• Закрепление анкеты выше в поиске\n"
        "• Быстрый отклик на вакансии\n"
        "• Доступ к закрытым вакансиям\n"
        "• Персональные предложения\n"
        "• Чат с работодателями\n"
        "• Бонусы за приглашённых водителей\n\n"
        "🛡 *При покупке годовой подписки:*\n"
        "• Скидка 10%\n"
        "• Цена зафиксирована, даже если стоимость вырастет"
    )

    await callback.message.edit_text(text, parse_mode="Markdown")
