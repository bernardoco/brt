from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import tasks


with DAG(
    'view_brt_data',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    },
    description='Simple BRT data visualization',
    schedule_interval='*/1 * * * *',
    start_date=datetime(2022, 3, 24),
    catchup=False,
    tags=['BRT'],
) as dag:

    fetch_json_task = PythonOperator(
        python_callable=tasks.fetch_json_data,
        op_kwargs={"url": 'http://webapibrt.rio.rj.gov.br/api/v1/brt'},
        task_id="fetch_json_task"
    )

    to_csv_task = PythonOperator(
        python_callable=tasks.save_to_csv,
        op_kwargs={"df": "{{task_instance.xcom_pull(task_ids='fetch_json_task')}}",
                    "filename": "output.csv"},
        task_id="to_csv_task"
    )


    fetch_json_task >> to_csv_task