# Usa l'immagine ufficiale di Apache Airflow
FROM apache/airflow:latest

# Imposta le variabili di ambiente per il database e timeout del webserver
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:////opt/airflow/airflow.db
ENV AIRFLOW__WEBSERVER__WEB_SERVER_WORKER_TIMEOUT=300
ENV AIRFLOW__WEBSERVER__WEB_SERVER_MASTER_TIMEOUT=300

# Crea le cartelle necessarie e assegna i permessi
RUN mkdir -p /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins

# Inizializza il database Airflow e crea un utente amministratore
RUN airflow db init && \
    airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Avvia sia il webserver sia lo scheduler
CMD ["bash", "-c", "sleep 30 && airflow webserver & airflow scheduler"]