import pandas as pd
import psycopg2
import os

def load_data():
    df = pd.read_csv('/opt/airflow/dags/etl/tmp/exchange_rates_transformed.csv')

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )
    cur = conn.cursor()

    for _, row in df.iterrows():
        # Insert currencies to dim_currency if not exists
        for currency in [row['base_currency'], row['target_currency']]:
            cur.execute("""
                INSERT INTO dim_currency (currency_code)
                VALUES (%s)
                ON CONFLICT (currency_code) DO NOTHING;
            """, (currency,))

        # Insert into dim_time
        cur.execute("""
            INSERT INTO dim_time (fetch_date, fetch_time)
            VALUES (%s, %s)
            ON CONFLICT (fetch_date, fetch_time) DO NOTHING
            RETURNING time_id;
        """, (row['fetch_date'], row['fetch_time']))
        result = cur.fetchone()
        if result:
            time_id = result[0]
        else:
            cur.execute("""
                SELECT time_id FROM dim_time WHERE fetch_date = %s AND fetch_time = %s
            """, (row['fetch_date'], row['fetch_time']))
            time_id = cur.fetchone()[0]

        # Insert into fact_exchange_rate
        cur.execute("""
            INSERT INTO fact_exchange_rate (base_currency, target_currency, rate, time_id, fetch_timestamp)
            VALUES (%s, %s, %s, %s, %s);
        """, (
            row['base_currency'],
            row['target_currency'],
            row['rate'],
            time_id,
            row['fetch_timestamp']
        ))

    conn.commit()
    cur.close()
    conn.close()

    # Simpan juga hasil final ke CSV untuk analitik
    df.to_csv('/opt/airflow/dags/etl/output/final_exchange_rates.csv', index=False)
