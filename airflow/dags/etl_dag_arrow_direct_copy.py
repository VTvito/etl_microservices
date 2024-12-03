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

def extract_clean_load(**kwargs):
    try:
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

        # Caricare i dati
        desired_format = 'csv'  # Può essere 'csv', 'excel', 'json'
        load_response = requests.post(
            f"http://load-data-service:5009/load-data?format={desired_format}",
            data=cleaned_data,
            headers={"Content-Type": "application/vnd.apache.arrow.stream"}
        )
        load_response.raise_for_status()

        # Log del successo
        print(f"Load Data succeeded with status code: {load_response.status_code}")


    except Exception as e:
        # Log dell'errore e sollevamento dell'eccezione per far fallire il task
        print(f"ETL process failed: {str(e)}")
        raise

with DAG('etl_direct_pipeline_copy', default_args=default_args, schedule_interval=None) as dag:
    task_extract_clean_load = PythonOperator(
        task_id='extract_clean_load',
        python_callable=extract_clean_load,
        provide_context=True
    )
