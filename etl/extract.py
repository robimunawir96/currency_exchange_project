import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "IDR")
TARGET_CURRENCIES = os.getenv("TARGET_CURRENCIES", "USD,EUR,SGD").split(",")
API_KEY = os.getenv("API_KEY")

url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"

response = requests.get(url)
data = response.json()

# Filter hanya target currencies
filtered_rates = {currency: data["conversion_rates"].get(currency) for currency in TARGET_CURRENCIES}
result = {
    "base": BASE_CURRENCY,
    "date": data["time_last_update_utc"],
    "rates": filtered_rates
}

# Simpan ke file
os.makedirs("data", exist_ok=True)
with open("data/raw_exchange.json", "w") as f:
    json.dump(result, f, indent=4)

print("[extract] Sukses menyimpan raw_exchange.json")
