from flask import Blueprint, jsonify, request
from app.transformation import apply_transformations
import pandas as pd
import os

bp = Blueprint('transformation', __name__)

DATA_FOLDER = '/app/data'

@bp.route('/transform_after_extract', methods=['POST'])
def transform_extracted_data():
    try:
        extracted_file_path = os.path.join(DATA_FOLDER, 'extracted_data.csv')
        if not os.path.exists(extracted_file_path):
            return jsonify({"status": "error", "message": "Nessun dato disponibile"}), 400

        # Lettura dei dati estratti
        extracted_data = pd.read_csv(extracted_file_path)
        transformed_data = apply_transformations(extracted_data)

        # Salvataggio dei dati trasformati
        transformed_file_path = os.path.join(DATA_FOLDER, 'transformed_data.csv')
        transformed_data.to_csv(transformed_file_path, index=False)

        return jsonify({
            "status": "success",
            "transformed_data": transformed_data.head().to_dict()
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/gettransformed', methods=['GET'])
def get_transformed_data():
    try:
        transformed_file_path = os.path.join(DATA_FOLDER, 'transformed_data.csv')
        if not os.path.exists(transformed_file_path):
            return jsonify({"status": "error", "message": "Nessun dato trasformato disponibile"}), 400

        transformed_data = pd.read_csv(transformed_file_path)
        return jsonify(transformed_data.to_dict()), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500