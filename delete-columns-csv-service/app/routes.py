from flask import Blueprint, jsonify, request
from app.columns import delete_columns_from_csv
import os
import pandas as pd

bp = Blueprint('delete-columns-csv', __name__)

DATA_FOLDER = '/app/data'

@bp.route('/delete-columns-csv', methods=['POST'])
def delete_columns():
    try:
        # Parametri dinamici dal body della richiesta
        dataset_name = request.json.get('dataset', 'dataset_name')
        client_id = request.json.get('client_id', 'client_id')
        columns_to_delete = request.json.get('columns')
        file_path = request.json.get('file_path')

        if not file_path or not columns_to_delete:
            return jsonify({"error": "Parametri 'file_path' e 'columns' sono richiesti"}), 400

        # Crea la cartella per i dati trasformati del cliente se non esiste
        client_folder = os.path.join(DATA_FOLDER, client_id, 'delete-columns-csv')
        os.makedirs(client_folder, exist_ok=True)

        # Rimuove le colonne specificate dal file CSV
        updated_file_path = delete_columns_from_csv(file_path, columns_to_delete)

        # Salva il CSV aggiornato nella cartella specifica del cliente
        transformed_file_path = os.path.join(client_folder, f'{dataset_name}.csv')
        pd.read_csv(updated_file_path).to_csv(transformed_file_path, index=False)

        return jsonify({
            "status": "success",
            "file_path": transformed_file_path
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/get-delete-columns-csv/<client_id>/<dataset_name>', methods=['GET'])
def get_deleted_columns_data(client_id, dataset_name):
    try:
        # Percorso dinamico per il file aggiornato
        transformed_file_path = os.path.join(DATA_FOLDER, client_id, 'delete-columns-csv', f'{dataset_name}.csv')
        
        if not os.path.exists(transformed_file_path):
            return jsonify({"status": "error", "message": "Dati aggiornati non disponibili"}), 400

        # Carica e restituisce i dati trasformati
        transformed_data = pd.read_csv(transformed_file_path)
        return jsonify(transformed_data.to_dict()), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500