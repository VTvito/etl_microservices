from flask import Blueprint, jsonify, request
from app.extract import process_excel
import os
import pandas as pd

bp = Blueprint('extract-excel', __name__)

DATA_FOLDER = '/app/data'

@bp.route('/extract-excel', methods=['POST'])
def extract_excel():
    try:
        # Parametri dinamici dal body della richiesta
        client_id = request.json.get('client_id', 'client_id')
        dataset_name = request.json.get('dataset', 'dataset_name')
        file_path = request.json.get('file_path')

        if not file_path:
            return jsonify({"error": "Il parametro file_path è richiesto"}), 400

        # Processa il file Excel
        data = process_excel(file_path)

        # Crea una cartella per il cliente se non esiste e salva i dati come CSV
        client_folder = os.path.join(DATA_FOLDER, client_id, 'extract-excel')
        os.makedirs(client_folder, exist_ok=True)
        file_path_csv = os.path.join(client_folder, f'{dataset_name}.csv')
        data.to_csv(file_path_csv, index=False)

        return jsonify({
            "status": "success",
            "data_preview": data.head().to_dict(),
            "file_path": file_path_csv
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route('/get-extract-excel/<client_id>/<dataset_name>', methods=['GET'])
def get_extracted_data(client_id, dataset_name):
    try:
        # Percorso del file salvato
        file_path_csv = os.path.join(DATA_FOLDER, client_id, 'extract-excel', f'{dataset_name}.csv')
        if not os.path.exists(file_path_csv):
            return jsonify({"error": "File non trovato"}), 404

        data = pd.read_csv(file_path_csv)
        return jsonify(data.to_dict()), 200
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