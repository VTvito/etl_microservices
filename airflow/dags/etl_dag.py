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
    'sample_etl_pipeline_2',
    default_args=default_args,
    description='Sample ETL Pipeline using Microservices',
    schedule_interval=None,  # Trigger manuale
)

# Funzioni per chiamare i microservizi

def read_csv_service(**context):
    url = 'http://read-csv-service:5001/read-csv'
    data = {
        'client_id': 'client1',
        'dataset': 'test_dataset',
        'file_path': '/app/data/test_dataset.csv'  # Percorso fisso del file di input
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    file_path = response.json().get("file_path")
    context['ti'].xcom_push(key='file_path', value=file_path)

def clean_nan_csv_service(**context):
    url = 'http://clean-nan-csv-service:5002/clean-nan-csv'
    file_path = context['ti'].xcom_pull(key='file_path', task_ids='read_csv_service')
    data = {
        'client_id': 'client1',
        'dataset': 'test_dataset',
        'file_path': file_path
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    file_path = response.json().get("file_path")
    context['ti'].xcom_push(key='file_path', value=file_path)

def get_columns_service(**context):
    url = 'http://get-columns-csv-service:5003/get-columns-csv'
    file_path = context['ti'].xcom_pull(key='file_path', task_ids='clean_nan_csv_service')
    data = {
        'client_id': 'client1',
        'dataset': 'test_dataset',
        'file_path': file_path
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    columns = response.json().get("columns")
    print(f"Columns: {columns}")

# Definizione delle task
read_task = PythonOperator(
    task_id='read_csv_service',
    python_callable=read_csv_service,
    provide_context=True,
    dag=dag,
)

clean_task = PythonOperator(
    task_id='clean_nan_csv_service',
    python_callable=clean_nan_csv_service,
    provide_context=True,
    dag=dag,
)

columns_task = PythonOperator(
    task_id='get_columns_service',
    python_callable=get_columns_service,
    provide_context=True,
    dag=dag,
)

# Ordine di esecuzione delle task
read_task >> clean_task >> columns_task