import os
import json
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# DB configs
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

# Load raw data
with open("data/raw_exchange.json", "r") as f:
    raw_data = json.load(f)

# Transform jadi dataframe
records = []
for currency, rate in raw_data["rates"].items():
    records.append({
        "base_currency": raw_data["base"],
        "target_currency": currency,
        "rate": rate,
        "date": raw_data["date"]
    })

df = pd.DataFrame(records)

# Simpan ke CSV
os.makedirs("output", exist_ok=True)
csv_path = "output/exchange_rates.csv"
df.to_csv(csv_path, index=False)
print(f"[transform] Data disimpan ke {csv_path}")

# Simpan ke PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    # Create table jika belum ada
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS exchange_rates (
        id SERIAL PRIMARY KEY,
        base_currency VARCHAR(3),
        target_currency VARCHAR(3),
        rate NUMERIC,
        date TIMESTAMP
    );
    """
    cur.execute(create_table_sql)

    # Insert data
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO exchange_rates (base_currency, target_currency, rate, date)
            VALUES (%s, %s, %s, %s)
        """, (row["base_currency"], row["target_currency"], row["rate"], row["date"]))

    conn.commit()
    cur.close()
    conn.close()
    print("[load] Data berhasil dimasukkan ke PostgreSQL")

except Exception as e:
    print(f"[load] Gagal memasukkan data ke PostgreSQL: {e}")
