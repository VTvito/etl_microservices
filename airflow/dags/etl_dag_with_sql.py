from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests

# Configurazione di base
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'etl_pipeline_with_sql',
    default_args=default_args,
    description='ETL Pipeline including SQL data extraction',
    schedule_interval=None,  # Trigger manuale
)

# Funzione per chiamare il microservizio SQL
def extract_sql_service(**context):
    url = 'http://extract-sql-service:5005/extract-sql'
    data = {
        'client_id': 'test_client',
        'query': 'SELECT * FROM example_table',
        'db_url': 'postgresql://airflow:airflow@postgres:5432/test_db',
        'db_name': 'test_db'
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    file_path = response.json().get("file_path")
    context['ti'].xcom_push(key='file_path', value=file_path)

# Funzione per chiamare il servizio di pulizia (esempio)
def clean_nan_service(**context):
    url = 'http://clean-nan-csv-service:5002/clean-nan-csv'
    file_path = context['ti'].xcom_pull(key='file_path', task_ids='extract_sql_service')
    data = {
        'client_id': 'test_client',
        'dataset': 'test_db',
        'file_path': file_path,
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    file_path = response.json().get("file_path")
    context['ti'].xcom_push(key='file_path', value=file_path)

# Task del DAG
extract_task = PythonOperator(
    task_id='extract_sql_service',
    python_callable=extract_sql_service,
    provide_context=True,
    dag=dag,
)

clean_task = PythonOperator(
    task_id='clean_nan_service',
    python_callable=clean_nan_service,
    provide_context=True,
    dag=dag,
)

# Definizione dell'ordine
extract_task >> clean_task
