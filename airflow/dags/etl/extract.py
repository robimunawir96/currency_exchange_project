# airflow/dags/etl/extract.py

import requests
import os
import pandas as pd

def extract_exchange_rates():
    base_currency = "IDR"
    target_currencies = ["USD", "EUR", "SGD", "JPY", "GBP"]
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    rates = []
    for currency in target_currencies:
        rate = data['conversion_rates'].get(currency)
        if rate:
            rates.append({
                'base_currency': base_currency,
                'target_currency': currency,
                'rate': rate,
                'fetch_timestamp': pd.Timestamp.now()
            })

    df = pd.DataFrame(rates)
    df.to_csv('/opt/airflow/dags/etl/tmp/exchange_rates_raw.csv', index=False)
