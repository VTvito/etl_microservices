# Progetto ETL a Microservizi su Kubernetes con Monitoraggio e Persistenza
Il progetto consiste nella costruzione di un'architettura ETL (Extract, Transform, Load) basata su microservizi orchestrati tramite Airflow.
I microservizi sono containerizzati con Docker e successivamente deployiati su Kubernetes. 
L'architettura è monitorata attraverso Prometheus e Grafana, 
con persistenza dei dati garantita da Postgres per il database di Airflow e volumi persistenti per DAG e dati condivisi.

---

## 1. Architettura

L'architettura è suddivisa nei seguenti componenti principali:

### MICROSERVIZI ETL:
1. **read-csv-service**: Estrae i dati da file CSV.
2. **clean-nan-csv-service**: Rimuove valori NaN dai dati.
3. **get-columns-csv-service**: Recupera le colonne specifiche del dataset.
4. **delete-columns-csv-service**: Elimina colonne indesiderate.

I microservizi sono strutturati in modo modulare, separando la logica di instradamento (**routes**) dalla logica di manipolazione dei dati. Utilizzano **Flask** come webserver.

---

### AIRFLOW:
- Gestisce i **DAG** (Direct Acyclic Graphs) per l'orchestrazione delle operazioni ETL.
- Utilizza **Postgres** per la persistenza.

---

### MONITORAGGIO CON PROMETHEUS E GRAFANA:
- **Prometheus**: Raccoglie metriche da Airflow e dai microservizi.
- **Grafana**: Visualizza le metriche e permette di creare dashboard interattive.

---

### DATABASE:
- **Postgres** per la persistenza del database Airflow.

---

## 2. Guida all'Installazione

### Requisiti:
- **Docker Desktop**
- **Kubernetes** (Minikube o Docker Desktop)
- **Helm** (per gestione avanzata dei manifest, da integrare)

---

### Esecuzione su Docker

1. **Clona il repository**:
   ```bash
   git clone <repository-url>
   cd etl_microservices

2. **Costruisci le immigini Docker e avviale**:
   ```bash
   docker-compose build
   docker-compose up -d

3. **Inizializza il database Airflow e crea utente admin**:
  ```bash
  docker exec -it airflow airflow db init
  docker exec -it airflow airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com -–password admin
```

4. **Copia dei file (dataset e dag) nei volumi montati (vedi docker-compose per il percorso)**:
 ```bash
docker cp /path/to/local/file container_name:/path/in/container  

esempio per file: docker cp dataset_test.csv read-csv-service:/app/data  

esempio per i dag: docker cp airflow/dags/etl_dag.py airflow:/opt/airflow/dags  
 ```

# Accedi all'interfaccia web:

Airflow: http://localhost:8080  

Prometheus: http://localhost:9090  

Grafana: http://localhost:3000  


5. **Deployare su Kubernetes (da ridefinire ancora)**:
  ```bash
kubectl apply -f ./kubernetes
kubectl get pods
(controllo correttezza pods)


