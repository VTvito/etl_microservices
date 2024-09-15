from flask import Blueprint, jsonify, request
from app.transformation import apply_transformations
import pandas as pd

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