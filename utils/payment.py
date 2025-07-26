import httpx
import os
import uuid
import hmac
import hashlib
import json
from db import save_payment_log

# 🔐 Переменные окружения
CRYPTO_API_KEY = os.getenv("CRYPTOMUS_API_KEY")
CRYPTO_MERCHANT = os.getenv("CRYPTOMUS_MERCHANT")
CRYPTO_SECRET = os.getenv("CRYPTOMUS_SECRET")
CRYPTOMUS_CALLBACK_URL = os.getenv("CRYPTOMUS_CALLBACK_URL", "https://jobjetbot.onrender.com/cryptomus/webhook")

# ✅ Флаг активности платежей
PAYMENT_ENABLED = all([CRYPTO_API_KEY, CRYPTO_MERCHANT, CRYPTO_SECRET])

if not PAYMENT_ENABLED:
    print("⚠️ Ключи CRYPTOMUS не найдены. Платёжные функции временно отключены.")

# 🧮 Генерация подписи Cryptomus
def generate_signature(data: dict, secret: str) -> str:
    data_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return hmac.new(secret.encode(), data_str.encode(), hashlib.sha256).hexdigest()

# 🔗 Получение ссылки на оплату
async def create_payment_link(pool, user_id: int, role: str, amount: float, payment_type: str = "premium") -> str:
    if not PAYMENT_ENABLED:
        raise RuntimeError("⚠️ Платёжные функции отключены. Установите ключи Cryptomus в .env")

    url = "https://api.cryptomus.com/v1/payment"
    order_id = str(uuid.uuid4())

    payload = {
        "order_id": order_id,
        "amount": str(amount),
        "currency": "USDT",
        "network": "TRC20",
        "url_return": "https://t.me/JobJetStarBot",
        "callback_url": CRYPTOMUS_CALLBACK_URL,
        "lifetime": 900,
        "to_currency": "USDT",
        "is_payment_multiple": False,
        "custom": {
            "user_id": user_id,
            "role": role,
            "payment_type": payment_type
        }
    }

    signature = generate_signature(payload, CRYPTO_SECRET)

    headers = {
        "merchant": CRYPTO_MERCHANT,
        "sign": signature,
        "Content-Type": "application/json",
        "api-key": CRYPTO_API_KEY
    }

    # 📡 Запрос на создание счёта
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    if "result" not in data or "url" not in data["result"]:
        raise Exception(f"❌ Ошибка создания платежа: {data}")

    # 💾 Логируем создание
    await save_payment_log(pool, user_id, role, amount, "USDT", "cryptomus", payment_type)

    return data["result"]["url"]
