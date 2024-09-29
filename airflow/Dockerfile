# Use the official Apache Airflow image as a base
FROM apache/airflow:latest

# Set the environment variable for the Airflow database
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:////opt/airflow/airflow.db

# Create necessary directories for volumes
RUN mkdir -p /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins

# Copy your DAGs, plugins, and other required files
# You can uncomment these lines if you have DAGs or plugins to copy during the build
COPY ./dags /opt/airflow/dags
COPY ./plugins /opt/airflow/plugins

# Initialize the Airflow database and create the admin user
RUN airflow db init && \
    airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Set the entry point to start both the webserver and the scheduler
CMD ["bash", "-c", "airflow webserver & airflow scheduler"]
