from flask import Blueprint, jsonify, request
from app.clean import apply_transformations
import pandas as pd
import os

bp = Blueprint('clean-nan-csv', __name__)

DATA_FOLDER = '/app/data'

@bp.route('/clean-nan-csv', methods=['POST'])
def transform_extracted_data():
    try:
        # Parametri dinamici dal body della richiesta
        dataset_name = request.json.get('dataset', 'dataset_name')
        client_id = request.json.get('client_id', 'client_id')
        file_path = request.json.get('file_path')  # Percorso file passato dall'utente
    
        if not file_path:
            return jsonify({"error": "Il parametro file_path è richiesto"}), 400

        # Carica i dati e applica la trasformazione per rimuovere i valori NaN
        extracted_data = pd.read_csv(file_path)
        transformed_data = apply_transformations(extracted_data)

        # Crea la cartella del cliente se non esiste già
        client_folder = os.path.join(DATA_FOLDER, client_id, 'clean-nan-csv')
        os.makedirs(client_folder, exist_ok=True)
        
        # Salva i dati trasformati con suffisso `_transformed_data.csv`
        transformed_file_path = os.path.join(client_folder, f'{dataset_name}.csv')
        transformed_data.to_csv(transformed_file_path, index=False)

        return jsonify({
            "status": "success",
            "transformed_data": transformed_data.head().to_dict(),  # Anteprima dei dati trasformati
            "file_path": transformed_file_path
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/get-clean-nan-csv/<client_id>/<dataset_name>', methods=['GET'])
def get_transformed_data(client_id, dataset_name):
    try:
        # Percorso dinamico del file trasformato
        transformed_file_path = os.path.join(DATA_FOLDER, client_id, 'clean-nan-csv', f'{dataset_name}.csv')
        
        # Verifica se il file di output esiste
        if not os.path.exists(transformed_file_path):
            return jsonify({"status": "error", "message": "Nessun dato trasformato disponibile"}), 400

        # Carica e restituisce i dati trasformati
        transformed_data = pd.read_csv(transformed_file_path)
        return jsonify(transformed_data.to_dict()), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

# Endpoint per il monitoraggio
from prometheus_client import Counter, generate_latest
from flask import Response

REQUEST_COUNTER = Counter('service_requests_total', 'Total number of requests for this service')

@bp.route('/metrics', methods=['GET'])
def metrics():
    REQUEST_COUNTER.inc()  # Incrementa ogni volta che viene richiesta la metrica
    return Response(generate_latest(), mimetype="text/plain")