from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="currency_exchange_etl",
    default_args=default_args,
    description="ETL DAG for Currency Exchange Rate with 2 tasks",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["currency", "exchange", "ETL"],
) as dag:

    extract_task = BashOperator(
        task_id="extract_exchange_rate",
        bash_command="python /opt/airflow/etl/extract.py"
    )

    transform_load_task = BashOperator(
        task_id="transform_and_load",
        bash_command="python /opt/airflow/etl/transform_load.py"
    )

    extract_task >> transform_load_task
