from aiogram import Router, types
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "referral_links")
async def show_referral_links(callback: CallbackQuery):
    await callback.answer()

    text = (
        "🎁 *Бонусы и скидки для водителей:*\n\n"
        "🔗 [WhiteBird](https://whitebird.io/?refid=jEYdB)\n"
        "💸 Удобные переводы, выгодные курсы, криптокошелёк\n\n"
        "🔗 [PaySend](https://paysend.com/referral/05ql7b)\n"
        "💳 Мгновенные переводы с карты на карту по всему миру\n\n"
        "🔗 [OKX](https://okx.com/join/72027985)\n"
        "📈 Крупная криптобиржа с бонусами за регистрацию\n\n"
        "🔗 [Cryptomus](https://app.cryptomus.com/signup?ref=wxkylP)\n"
        "🧾 Платежи в криптовалюте, быстрый вывод и защита"
    )

    await callback.message.edit_text(text, parse_mode="Markdown", disable_web_page_preview=True)
