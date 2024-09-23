from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests

# Definire il DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'etl_microservice_dag',
    default_args=default_args,
    description='DAG for ETL using microservices',
    schedule_interval=None,  # Manual trigger
)

# Funzione per chiamare il microservizio di estrazione
def call_extraction_service():
    url = 'http://extraction_service:5001/extract'
    payload = {
        "dataset": "example_dataset",
        "dataset_params": {
            "file_path": "/app/data/number.csv"
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Verifica che non ci siano errori
    print(f"Extraction Response: {response.json()}")
    return response.json()

# Funzione per chiamare il microservizio di trasformazione
def call_transformation_service():
    url = 'http://transformation_service:5002/transform_after_extract'
    response = requests.post(url)
    response.raise_for_status()  # Verifica che non ci siano errori
    print(f"Transformation Response: {response.json()}")
    return response.json()

# Task per l'estrazione
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=call_extraction_service,
    dag=dag,
)

# Task per la trasformazione
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=call_transformation_service,
    dag=dag,
)

# Definire la dipendenza delle task (prima estrazione, poi trasformazione)
extract_task >> transform_task
