import httpx
import os
import uuid
import json
import hmac
import hashlib

CRYPTO_API_KEY = os.getenv("CRYPTOMUS_API_KEY")
CRYPTO_MERCHANT = os.getenv("CRYPTOMUS_MERCHANT")

def generate_signature(payload: dict, api_key: str) -> str:
    body = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
    return hmac.new(api_key.encode(), body.encode(), hashlib.sha256).hexdigest()

async def create_payment_link(user_id: int, role: str, amount: float, payment_type: str):
    url = "https://api.cryptomus.com/v1/payment"

    payload = {
        "order_id": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "USDT",
        "network": "TRC20",
        "url_return": "https://t.me/JobJetStarBot",
        "lifetime": 900,
        "to_currency": "USDT",
        "is_payment_multiple": False,
        "custom_fields": {
            "user_id": str(user_id),
            "role": role,
            "payment_type": payment_type
        }
    }

    headers = {
        "merchant": CRYPTO_MERCHANT,
        "sign": generate_signature(payload, CRYPTO_API_KEY),
        "Content-Type": "application/json",
        "api-key": CRYPTO_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        data = response.json()

    if response.status_code == 200 and data.get("result") and data["result"].get("url"):
        return data["result"]["url"]
    else:
        print("❌ Ошибка создания платежа:", data)
        return None
