from flask import Blueprint, jsonify, request
from app.datasets import load_csv

bp = Blueprint('extraction', __name__)

# gloval variable to keept temporary the data extracted
extracted_data = None

# endpoint to receive the data from POST
@bp.route('/extract', methods=['POST'])
def extract_dataset():

    global extracted_data
    
    try:
        dataset_name = request.json.get('dataset')
        dataset_params = request.json.get('dataset_params')

        if not dataset_name or not dataset_params:
            return jsonify({"error": "Dataset name and parameters are required"}), 400

        # Extract the dataset by using defined loading function from datasets.py
        extracted_data = load_csv(dataset_params['file_path'])
        
        return jsonify({
            "status": "success",
            "data_preview": extracted_data.head().to_dict()  # Show the first 5 records
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# exposition of endpoint data - API call from other microservices # to complete
@bp.route('/getdata', methods=['GET'])
def getdata():
    
    global extracted_data
    
    if extracted_data is None:
        return jsonify({"status":"error", "message":"No data available"}), 400
    
    # Return extracted data like JSON
    return jsonify(extracted_data.to_dict()), 200


# extra fetures to complete --> show html page with datasample
"""
@bp.route('/showdata', methods=['GET'])
def showdata():
    print(extracted_data)
"""