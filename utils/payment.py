import httpx
import os
import uuid
import hmac
import hashlib
import json

CRYPTO_API_KEY = os.getenv("CRYPTOMUS_API_KEY")
CRYPTO_MERCHANT = os.getenv("CRYPTOMUS_MERCHANT")
CRYPTO_SECRET = os.getenv("CRYPTOMUS_SECRET")

# 🧮 Генерация подписи Cryptomus
def generate_signature(data: dict, secret: str) -> str:
    data_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return hmac.new(secret.encode(), data_str.encode(), hashlib.sha256).hexdigest()

# 🔗 Получение ссылки на оплату
async def create_payment_link(user_id: int, role: str, amount: float, payment_type: str) -> str:
    url = "https://api.cryptomus.com/v1/payment"

    payload = {
        "order_id": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "USDT",
        "network": "TRC20",
        "url_return": "https://t.me/JobJetStarBot",
        "lifetime": 900,
        "to_currency": "USDT",
        "is_payment_multiple": False
    }

    signature = generate_signature(payload, CRYPTO_SECRET)

    headers = {
        "merchant": CRYPTO_MERCHANT,
        "sign": signature,
        "Content-Type": "application/json",
        "api-key": CRYPTO_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    return data["result"]["url"]
