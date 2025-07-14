import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import setup_application

TOKEN = "7883161984:AAF_T1IMahf_EYS42limVzfW-5NGuyNu0Qk"
BASE_WEBHOOK_URL = "https://jobjetbot.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.update()
async def echo_all(update: Update):
    print("🔔 Апдейт получен от Telegram:")
    print(update.model_dump_json(indent=2))

async def on_startup(app: web.Application):
    print("🚀 BOT STARTED")
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"🔗 Webhook установлен: {WEBHOOK_URL}")
    else:
        print("✅ Webhook уже активен")

async def on_shutdown(app: web.Application):
    print("🛑 BOT STOPPED")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, dp, bot=bot)
    app.router.add_get("/", lambda _: web.Response(text="Test webhook is active."))
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
