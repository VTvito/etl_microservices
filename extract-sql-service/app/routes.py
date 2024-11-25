from flask import Blueprint, jsonify, request
from app.extract import extract_from_sql
import os
import pandas as pd

bp = Blueprint('extract-sql', __name__)

DATA_FOLDER = '/app/data'

@bp.route('/extract-sql', methods=['POST'])
def extract_data():
    try:
        # Parametri dinamici dal body della richiesta
        client_id = request.json.get('client_id', 'client_id')
        query = request.json.get('query', 'SELECT * FROM table_name')  # Query SQL
        db_url = request.json.get('db_url')  # URL di connesssione al db
        db_name = request.json.get('db_name', 'db_name')
        
        if not db_url:
            return jsonify({"error": "Il parametro db_url è richiesto"}), 400

        # Estrazione dei dati
        data = extract_from_sql(db_url, query)

        # Crea una cartella specifica per il cliente se non esiste e salva il file in .csv
        client_folder = os.path.join(DATA_FOLDER, client_id, 'extract-sql')
        os.makedirs(client_folder, exist_ok=True)
        file_path = os.path.join(client_folder, f'{db_name}.csv')
        data.to_csv(file_path, index=False)

        return jsonify({
            "status": "success",
            "data_preview": data.head().to_dict(),
            "file_path": file_path
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route('/get-extract-sql/<client_id>/<db_name>', methods=['GET'])
def getdata(client_id, db_name):
    try:
        # Percorso specifico per cliente e dataset
        extracted_file_path = os.path.join(DATA_FOLDER, client_id, 'extract-sql', f'{db_name}.csv')
        
        if not os.path.exists(extracted_file_path):
            return jsonify({"status": "error", "message": "Nessun dato disponibile per questo dataset"}), 400

        extracted_data = pd.read_csv(extracted_file_path)
        return jsonify(extracted_data.to_dict()), 200

    except ConnectionError as ce:
        return jsonify({"status": "error", "message": str(ce)}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Endpoint per il monitoraggio
from prometheus_client import Counter, generate_latest
from flask import Response

REQUEST_COUNTER = Counter('service_requests_total', 'Total number of requests for this service')

@bp.route('/metrics', methods=['GET'])
def metrics():
    REQUEST_COUNTER.inc()
    return Response(generate_latest(), mimetype="text/plain")