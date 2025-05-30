# airflow/dags/etl/transform.py

import pandas as pd
import os

def transform_data():
    df = pd.read_csv('/opt/airflow/dags/etl/tmp/exchange_rates_raw.csv')
    df['fetch_date'] = pd.to_datetime(df['fetch_timestamp']).dt.date
    df['fetch_time'] = pd.to_datetime(df['fetch_timestamp']).dt.time

    # Save for loading step
    df.to_csv('/opt/airflow/dags/etl/tmp/exchange_rates_transformed.csv', index=False)
