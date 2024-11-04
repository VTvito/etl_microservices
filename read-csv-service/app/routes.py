from flask import Blueprint, jsonify, request
from app.read import load_csv
import os
import pandas as pd

bp = Blueprint('read-csv', __name__)

DATA_FOLDER = '/app/data'

@bp.route('/read-csv', methods=['POST'])
def extract_dataset():
    try:
        # Parametri dinamici dal body della richiesta
        dataset_name = request.json.get('dataset', 'dataset_name')
        client_id = request.json.get('client_id', 'client_id')
        file_path = request.json.get('file_path')
        
        if not file_path:
            return jsonify({"error": "Il parametro file_path è richiesto"}), 400

        # Crea una cartella specifica per il cliente se non esiste
        client_folder = os.path.join(DATA_FOLDER, client_id, 'read-csv')
        os.makedirs(client_folder, exist_ok=True)

        # Estrazione del dataset dal file specificato
        extracted_data = load_csv(file_path)

        # Salva il file elaborato nella cartella del servizio
        extracted_file_path = os.path.join(client_folder, f'{dataset_name}.csv')
        extracted_data.to_csv(extracted_file_path, index=False)

        return jsonify({
            "status": "success",
            "data_preview": extracted_data.head().to_dict(),
            "file_path": extracted_file_path
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/get-read-csv/<client_id>/<dataset_name>', methods=['GET'])
def getdata(client_id, dataset_name):
    try:
        # Percorso specifico per cliente e dataset
        extracted_file_path = os.path.join(DATA_FOLDER, client_id, 'read-csv', f'{dataset_name}.csv')
        
        if not os.path.exists(extracted_file_path):
            return jsonify({"status": "error", "message": "Nessun dato disponibile per questo dataset"}), 400

        extracted_data = pd.read_csv(extracted_file_path)
        return jsonify(extracted_data.to_dict()), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    
# Codice per il monitoraggio
from prometheus_client import Counter, generate_latest
from flask import Response

REQUEST_COUNTER = Counter('service_requests_total', 'Total number of requests for this service')

@bp.route('/metrics', methods=['GET'])
def metrics():
    REQUEST_COUNTER.inc()  # Incrementa ogni volta che viene richiesta la metrica
    return Response(generate_latest(), mimetype="text/plain")