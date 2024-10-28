from flask import Blueprint, jsonify, request
from app.datasets import load_csv
import os
import pandas as pd

bp = Blueprint('extraction', __name__)

DATA_FOLDER = '/app/data'

@bp.route('/extract', methods=['POST'])
def extract_dataset():
    try:
        dataset_name = request.json.get('dataset')
        dataset_params = request.json.get('dataset_params')

        if not dataset_name or not dataset_params:
            return jsonify({"error": "Nome del dataset e parametri sono richiesti"}), 400

        # Estrazione del dataset
        extracted_data = load_csv(dataset_params['file_path'])

        # Salvataggio del dataset estratto come file CSV nel volume condiviso
        extracted_file_path = os.path.join(DATA_FOLDER, 'extracted_data.csv')
        extracted_data.to_csv(extracted_file_path, index=False)

        return jsonify({
            "status": "success",
            "data_preview": extracted_data.head().to_dict()  # Mostra i primi 5 record
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/getdata', methods=['GET'])
def getdata():
    try:
        extracted_file_path = os.path.join(DATA_FOLDER, 'extracted_data.csv')
        if not os.path.exists(extracted_file_path):
            return jsonify({"status": "error", "message": "Nessun dato disponibile"}), 400

        extracted_data = pd.read_csv(extracted_file_path)
        return jsonify(extracted_data.to_dict()), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500