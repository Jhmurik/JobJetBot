import httpx
import os
import uuid

CRYPTO_API_KEY = os.getenv("CRYPTOMUS_API_KEY")
CRYPTO_MERCHANT = os.getenv("CRYPTOMUS_MERCHANT")

async def create_payment_link(user_id: int, role: str, amount: float, payment_type: str):
    url = "https://api.cryptomus.com/v1/payment"

    payload = {
        "order_id": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "USDT",
        "network": "TRC20",
        "url_return": "https://t.me/JobJetStarBot",  # сюда можно вставить URL кнопки
        "lifetime": 900,
        "to_currency": "USDT",
        "is_payment_multiple": False
    }

    headers = {
        "merchant": CRYPTO_MERCHANT,
        "sign": "",
        "Content-Type": "application/json",
        "api-key": CRYPTO_API_KEY
    }

    # 💰 Вычислим подпись (если потребуется — добавим функцию)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        data = response.json()

    return data["result"]["url"]
