from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

# Configurazione di base
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 1),
    'retries': 1,
}

def extract_clean_load(**kwargs):
    try:
        # Estrarre i dati
        extract_data = {
            "client_id": "airflow_client",
            "file_path": "/app/data/test_dataset.csv"  # Percorso all'interno del container
        }
        print("Invio richiesta a extract-csv-service...")
        extract_response = requests.post("http://extract-csv-service:5001/extract-csv", json=extract_data)
        print(f"Risposta extract-csv-service: {extract_response.status_code}")
        extract_response.raise_for_status()
        ipc_data = extract_response.content
        print(f"Dati IPC estratti: {len(ipc_data)} bytes")

        # Pulire i dati
        print("Invio richiesta a clean-nan-service...")
        clean_response = requests.post(
            "http://clean-nan-service:5002/clean-nan",
            data=ipc_data,
            headers={"Content-Type": "application/vnd.apache.arrow.stream"}
        )
        print(f"Risposta clean-nan-service: {clean_response.status_code}")
        clean_response.raise_for_status()
        cleaned_data = clean_response.content
        print(f"Dati puliti: {len(cleaned_data)} bytes")

        # Caricare i dati
        desired_format = 'csv'  # Può essere 'csv', 'excel', 'json'
        print(f"Invio richiesta a load-data-service con formato {desired_format}...")
        load_response = requests.post(
            f"http://load-data-service:5009/load-data?format={desired_format}",
            data=cleaned_data,
            headers={"Content-Type": "application/vnd.apache.arrow.stream"}
        )
        print(f"Risposta load-data-service: {load_response.status_code}")
        load_response.raise_for_status()

        # Estrarre il messaggio di conferma
        response_json = load_response.json()
        if response_json.get("status") == "success":
            file_saved = response_json.get("message")
            print(f"Load Data succeeded: {file_saved}")
            # Puoi anche salvare il percorso del file in XCom per utilizzarlo in altri task
            # kwargs['ti'].xcom_push(key='loaded_file', value=file_saved)
        else:
            print(f"Load Data failed: {response_json.get('message')}")
            raise Exception(f"Load Data failed: {response_json.get('message')}")

    except Exception as e:
        # Log dell'errore e sollevamento dell'eccezione per far fallire il task
        print(f"ETL process failed: {str(e)}")
        raise

with DAG('etl_arrow_direct_v2', default_args=default_args, schedule_interval=None) as dag:
    task_extract_and_clean = PythonOperator(
        task_id='extract_clean_load',
        python_callable=extract_clean_load,
        provide_context=True
    )