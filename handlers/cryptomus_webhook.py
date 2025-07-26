# handlers/cryptomus_webhook.py

from aiohttp import web
import hmac
import hashlib
import json
import os

from db import save_payment, confirm_payment  # confirm_payment должен быть реализован

# 🔐 Переменные окружения (можно оставить тестовые значения)
CRYPTOMUS_API_KEY = os.getenv("CRYPTOMUS_API_KEY", "test_key")
CRYPTOMUS_MERCHANT = os.getenv("CRYPTOMUS_MERCHANT", "test_merchant")

# 📡 Роутер
cryptomus_webhook = web.RouteTableDef()

@cryptomus_webhook.post("/webhook/cryptomus")
async def handle_cryptomus_webhook(request: web.Request):
    try:
        raw_body = await request.read()
        headers = request.headers
        received_sign = headers.get("sign")

        if not received_sign:
            return web.Response(status=401, text="Missing sign")

        generated_sign = hmac.new(
            CRYPTOMUS_API_KEY.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()

        if received_sign != generated_sign:
            return web.Response(status=401, text="Invalid signature")

        data = json.loads(raw_body)

        if data.get("status") != "paid":
            return web.Response(status=200, text="Ignored")

        custom = data.get("custom", {})
        user_id = int(custom.get("user_id", 0))
        role = custom.get("role", "driver")
        payment_type = custom.get("payment_type", "premium")

        amount = float(data.get("amount", 0))
        currency = data.get("currency", "USDT")
        method = data.get("payment_method", "cryptomus")
        description = f"Оплата подписки ({role})"

        pool = request.app["db"]

        await save_payment(
            pool, user_id, role, amount, currency,
            method, payment_type, description
        )

        await confirm_payment(pool, user_id, role, amount, payment_type)

        return web.Response(status=200, text="OK")

    except Exception as e:
        print(f"[Cryptomus Webhook Error] {e}")
        return web.Response(status=500, text=f"Internal error: {e}")
