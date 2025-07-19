from aiohttp import web
import hmac
import hashlib
import json
import os
from db import save_payment
from uuid import UUID

CRYPTOMUS_API_KEY = os.getenv("CRYPTOMUS_API_KEY")
CRYPTOMUS_MERCHANT = os.getenv("CRYPTOMUS_MERCHANT")

# 📩 Обработчик входящих webhook от Cryptomus
async def handle_cryptomus_webhook(request: web.Request):
    try:
        data = await request.json()
        headers = request.headers

        # ✅ Проверка подписи
        received_sign = headers.get("sign")
        if not received_sign:
            return web.Response(status=401, text="Missing sign")

        raw_body = await request.read()
        generated_sign = hmac.new(
            CRYPTOMUS_API_KEY.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()

        if received_sign != generated_sign:
            return web.Response(status=401, text="Invalid signature")

        # 📥 Обработка успешной оплаты
        if data["status"] == "paid":
            metadata = data.get("order_id", "")
            user_id = int(data["custom"]["user_id"])
            role = data["custom"]["role"]
            payment_type = data["custom"]["payment_type"]

            amount = float(data["amount"])
            currency = data["currency"]
            method = data.get("payment_method", "cryptomus")

            pool = request.app["db"]
            await save_payment(pool, {
                "user_id": user_id,
                "role": role,
                "amount": amount,
                "currency": currency,
                "payment_method": method,
                "payment_type": payment_type,
                "description": f"Оплата подписки {role}"
            })

            # 🔐 TODO: тут можно активировать подписку в базе

            return web.Response(status=200, text="OK")

        return web.Response(status=200, text="Ignored")
    except Exception as e:
        return web.Response(status=500, text=f"Internal error: {str(e)}")
