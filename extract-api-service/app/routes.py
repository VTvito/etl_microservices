from flask import Blueprint, jsonify, request
from app.extract import extract_from_api
import os
import pandas as pd

bp = Blueprint('extract-api', __name__)

DATA_FOLDER = '/app/data'

@bp.route('/extract-api', methods=['POST'])
def api_extraction():
    try:
        # Parametri dinamici dal body della richiesta
        client_id = request.json.get('client_id', 'client_id')
        api_url = request.json.get('api_url')
        api_params = request.json.get('api_params', {})
        auth_type = request.json.get('auth_type')  # Tipo di autenticazione
        auth_value = request.json.get('auth_value')  # Valore dell'autenticazione
        dataset_name = request.json.get('dataset', 'dataset_name')

        if not api_url:
            return jsonify({"error": "Il parametro api_url è richiesto"}), 400

        # Esegui l'estrazione
        data = extract_from_api(api_url, api_params, auth_type, auth_value)

        # Crea la cartella del cliente
        client_folder = os.path.join(DATA_FOLDER, client_id, 'extract-api')
        os.makedirs(client_folder, exist_ok=True)

        # Salva i dati come CSV
        file_path = os.path.join(client_folder, f'{dataset_name}.csv')
        data.to_csv(file_path, index=False)

        return jsonify({
            "status": "success",
            "data_preview": data.head().to_dict(),
            "file_path": file_path
        }), 200

    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    
# Endpoint per recuperare i dati estratti
@bp.route('/get-extract-api/<client_id>/<dataset_name>', methods=['GET'])
def get_extracted_data(client_id, dataset_name):
    try:
        file_path = os.path.join(DATA_FOLDER, client_id, 'extract-api', f'{dataset_name}.csv')
        if not os.path.exists(file_path):
            return jsonify({"error": "Dataset non trovato"}), 404

        data = pd.read_csv(file_path)
        return jsonify(data.to_dict()), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


from prometheus_client import Counter, generate_latest
from flask import Response

# Endpoint per il monitoraggio
REQUEST_COUNTER = Counter('service_requests_total', 'Total number of requests for this service')

@bp.route('/metrics', methods=['GET'])
def metrics():
    REQUEST_COUNTER.inc()
    return Response(generate_latest(), mimetype="text/plain")