from flask import Blueprint, jsonify, request
from app.upload import save_uploaded_file
import os

bp = Blueprint('upload-file', __name__)

@bp.route('/upload-file', methods=['POST'])
def upload_file():
    # Recupera parametri dalla richiesta
    client_id = request.form.get('client_id', 'default')
    dataset_name = request.form.get('dataset', 'dataset_name')

    # Verifica che il file sia presente nella richiesta
    if 'file' not in request.files:
        return jsonify({"error": "File non trovato nella richiesta"}), 400

    file = request.files['file']
    
    # Chiama la funzione per salvare il file e ottiene il percorso di salvataggio
    file_path = save_uploaded_file(file, client_id, dataset_name)
    
    return jsonify({"status": "success", "file_path": file_path}), 200
