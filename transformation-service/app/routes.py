from flask import Blueprint, jsonify, request
from app.transformation import apply_transformations
import pandas as pd
import requests

# creation of blueprint for the route of microservice
bp = Blueprint('transformation', __name__)

@bp.route('/transform', methods=['POST'])
def transform_data():
    try:     
        # data passed like JSON in body request of POST
        input_data = request.json

        df = pd.DataFrame(input_data)
    
        transformed_data = apply_transformations(df)

        # Return transformed data in JSON
        return jsonify({
            "status": "success",
            "transformed_data" : transformed_data.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# transform data by calling extraction service by API
@bp.route('/transform_after_extract', methods=['POST'])
def transform_extracted_data():

    try:
        # extract data from extraction_microservice
        extraction_response = requests.get('http://extraction-service:5001/getdata') # 127.0.0.1:5001

        if extraction_response.status_code != 200:
            return jsonify({"status":"error", "message":"Error during data extraction from GET"}), 500

        # convert data received in DataFrame Pandas
        extracted_data = extraction_response.json()

        df = pd.DataFrame(extracted_data)
        
        transformed_data = apply_transformations(df)

        # Return transformed data in JSON
        return jsonify({
            "status": "success",
            "transformed_data" : transformed_data.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500