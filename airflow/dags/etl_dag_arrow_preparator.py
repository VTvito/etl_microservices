from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
# Importiamo il Preparator dal percorso in cui lo abbiamo messo
# Se l'hai messo nella stessa cartella del DAG:
from preparator import Preparator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 1),
    'retries': 1,
}

def extract_clean_load(**kwargs):
    try:
        # Configurazione dei servizi
        services_config = {
            "extract": "http://extract-csv-service:5001/extract-csv",
            "clean": "http://clean-nan-service:5002/clean-nan",
            "load": "http://load-data-service:5009/load-data"
        }
        prep = Preparator(services_config)

        # Usa il Preparator invece dei requests diretti
        ipc_data = prep.extract("airflow_client", "/app/data/test_dataset.csv")
        cleaned_data = prep.clean(ipc_data)
        msg = prep.load(cleaned_data, format='csv')
        print(f"ETL succeeded: {msg}")

    except Exception as e:
        print(f"ETL process failed: {str(e)}")
        raise

with DAG('etl_dag_arrow_preparator', default_args=default_args, schedule_interval=None) as dag:
    task_extract_and_clean = PythonOperator(
        task_id='extract_clean_load',
        python_callable=extract_clean_load,
        provide_context=True
    )
