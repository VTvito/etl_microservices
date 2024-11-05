# Usa l'immagine ufficiale di Apache Airflow
FROM apache/airflow:latest

# Imposta le variabili di ambiente per il database e timeout del webserver
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:////opt/airflow/airflow.db
ENV AIRFLOW__WEBSERVER__WEB_SERVER_WORKER_TIMEOUT=300
ENV AIRFLOW__WEBSERVER__WEB_SERVER_MASTER_TIMEOUT=300

# Imposta le variabili per Prometheus e StatsD
ENV AIRFLOW__METRICS__STATSD_ON=True
ENV AIRFLOW__METRICS__STATSD_HOST=prometheus
ENV AIRFLOW__METRICS__STATSD_PORT=9125
ENV AIRFLOW__METRICS__STATSD_PREFIX=airflow

# Crea le cartelle necessarie e assegna i permessi
RUN mkdir -p /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins

# Inizializza il database Airflow solo se non esiste già
RUN if [ ! -f /opt/airflow/airflow.db ]; then \
    airflow db init && \
    airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin; \
    fi

# Avvia sia il webserver sia lo scheduler con un ritardo iniziale
CMD ["bash", "-c", "sleep 30 && airflow webserver & airflow scheduler"]