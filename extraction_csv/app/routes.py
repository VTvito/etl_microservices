from flask import Blueprint, jsonify, request
from app.datasets import load_csv

bp = Blueprint('extraction', __name__)

@bp.route('/extract', methods=['POST'])
def extract_dataset():
    try:
        dataset_name = request.json.get('dataset')
        dataset_params = request.json.get('dataset_params')

        if not dataset_name or not dataset_params:
            return jsonify({"error": "Dataset name and parameters are required"}), 400

        # Extract the dataset by using defined loading function from datasets.py
        data = load_csv(dataset_params['file_path'])
        
        return jsonify({
            "status": "success",
            "data_preview": data.head().to_dict()  # Show the first 5 records
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# exposition of endpoint data - API call from other microservices # still to complete
""""
@bp.route('/data', Method=['GET'])
def get_data():
    # Return extracted data like JSON
    return jsonify(extraced_data)
"""