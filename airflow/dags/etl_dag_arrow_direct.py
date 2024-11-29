from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

# Configurazione di base
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 1),
    'retries': 1,
}

dag = DAG(
    'etl_arrow_direct_pipeline',
    default_args=default_args,
    description='ETL Pipeline with Apache Arrow',
    schedule_interval=None,  # Trigger manuale
)

def extract_and_clean(**kwargs):
    # Estrarre i dati
    extract_data = {
        "client_id": "airflow_client",
        "file_path": "/app/data/test_dataset.csv"
    }
    extract_response = requests.post("http://extract-csv-service:5001/extract-csv", json=extract_data)
    extract_response.raise_for_status()
    ipc_data = extract_response.content

    # Pulire i dati
    clean_response = requests.post(
        "http://clean-nan-service:5002/clean-nan",
        data=ipc_data,
        headers={"Content-Type": "application/vnd.apache.arrow.stream"}
    )
    clean_response.raise_for_status()
    cleaned_data = clean_response.content

    # Log o ulteriori elaborazioni
    print(f"Cleaned data size: {len(cleaned_data)} bytes")

with DAG('etl_arrow_direct_pipeline', default_args=default_args, schedule_interval=None) as dag:
    task_extract_and_clean = PythonOperator(
        task_id='extract_and_clean',
        python_callable=extract_and_clean,
        provide_context=True
    )