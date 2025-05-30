# airflow/dags/fetch_exchange_rates_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from etl.extract import extract_exchange_rates
from etl.transform import transform_data
from etl.load import load_data

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='fetch_exchange_rates_dag',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    description='ETL DAG untuk fetch & simpan data nilai tukar',
    tags=['exchange_rate', 'currency', 'ETL']
) as dag:

    task_extract = PythonOperator(
        task_id='extract_exchange_rates',
        python_callable=extract_exchange_rates,
    )

    task_transform = PythonOperator(
        task_id='transform_exchange_rates',
        python_callable=transform_data,
    )

    task_load = PythonOperator(
        task_id='load_exchange_rates',
        python_callable=load_data,
    )

    task_extract >> task_transform >> task_load 
