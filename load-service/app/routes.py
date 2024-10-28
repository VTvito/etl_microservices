from flask import Blueprint, jsonify, request
from app.load import save_data
import os
import pandas as pd

bp = Blueprint('load', __name__)

@bp.route('/load', methods=['POST'])
def load_data():
    try:
        # Ricevere dati trasformati dal payload JSON
        transformed_data = request.json.get('transformed_data')
        
        if not transformed_data:
            return jsonify({"error": "Dati trasformati mancanti"}), 400
        
        # Salvataggio dei dati trasformati
        file_path = save_data(transformed_data)
        
        return jsonify({"status": "success", "message": f"Dati salvati in {file_path}"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
