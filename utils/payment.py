import httpx
import os
import uuid
import hmac
import hashlib
import json

# 🔐 Переменные окружения
CRYPTO_API_KEY = os.getenv("CRYPTOMUS_API_KEY")        # API ключ Cryptomus
CRYPTO_MERCHANT = os.getenv("CRYPTOMUS_MERCHANT")      # ID мерчанта
CRYPTO_SECRET = os.getenv("CRYPTOMUS_SECRET")          # Секрет для подписи

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
        "url_return": "https://t.me/JobJetStarBot",  # Ссылка возврата после оплаты
        "lifetime": 900,                             # Время жизни счёта (в секундах)
        "to_currency": "USDT",
        "is_payment_multiple": False
    }

    # ✍️ Генерация подписи
    signature = generate_signature(payload, CRYPTO_SECRET)

    headers = {
        "merchant": CRYPTO_MERCHANT,
        "sign": signature,
        "Content-Type": "application/json",
        "api-key": CRYPTO_API_KEY
    }

    # 📡 Запрос к API
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    if "result" not in data or "url" not in data["result"]:
        raise Exception(f"Ошибка создания платежа: {data}")

    return data["result"]["url"]
