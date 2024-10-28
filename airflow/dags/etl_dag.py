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
    description='DAG per ETL utilizzando microservizi',
    schedule_interval=None,  # Trigger manuale
)

# Funzione per chiamare il microservizio di estrazione
def call_extraction_service(**context):
    url = 'http://extraction-service:5001/extract'
    payload = {
        "dataset": "test_dataset",
        "dataset_params": {
            "file_path": "/app/data/number.csv",
            "source_type": "csv"
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Verifica che non ci siano errori
    print(f"Extraction Response: {response.json()}")
    # Passa il nome del dataset alla task successiva
    return payload["dataset"]

# Funzione per chiamare il microservizio di trasformazione
def call_transformation_service(**context):
    dataset = context['ti'].xcom_pull(task_ids='extract_data')
    url = 'http://transformation-service:5002/transform_after_extract'
    response = requests.post(url)
    response.raise_for_status()  # Verifica che non ci siano errori
    print(f"Transformation Response: {response.json()}")
    return response.json()

# Funzione per chiamare il microservizio di caricamento
def call_load_service(**context):
    transformed_data = context['ti'].xcom_pull(task_ids='transform_data')['transformed_data']
    url = 'http://load-service:5003/load'
    payload = {
        "transformed_data": transformed_data
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Verifica che non ci siano errori
    print(f"Load Response: {response.json()}")

# Task per l'estrazione
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=call_extraction_service,
    provide_context=True,
    dag=dag,
)

# Task per la trasformazione
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=call_transformation_service,
    provide_context=True,
    dag=dag,
)

# Task per il caricamento
load_task = PythonOperator(
    task_id='load_data',
    python_callable=call_load_service,
    provide_context=True,
    dag=dag,
)

# Definire la dipendenza delle task (estrazione -> trasformazione -> caricamento)
extract_task >> transform_task >> load_task