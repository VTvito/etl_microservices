from flask import Blueprint, jsonify, request
from app.read import load_csv_to_arrow, arrow_to_json
import pyarrow as pa

bp = Blueprint('extract-csv', __name__)

@bp.route('/extract-csv', methods=['POST'])
def extract_csv():
    """
    API Endpoint to extract data from a CSV file and process it into Apache Arrow format.

    Request Body:
    - client_id (str): ID of the client requesting the operation.
    - file_path (str): Path to the input CSV file.

    Returns:
    - JSON response containing:
      - status (str): "success" or "error".
      - data_preview (dict): First few rows of the dataset as a preview.
      - data_arrow (str): Serialized Arrow Table in JSON format.
    """
    try:
        # Get request parameters
        file_path = request.json.get('file_path')

        if not file_path:
            return jsonify({"error": "Parameter 'file_path' is required"}), 400

        # Load data into Arrow Table
        arrow_table = load_csv_to_arrow(file_path)

        # Serialize the Arrow Table to JSON
        arrow_json = arrow_to_json(arrow_table)

        return jsonify({
            "status": "success",
            "data_preview": arrow_table.to_pandas().head().to_dict(),
            "data_arrow": arrow_json  # Arrow Table serialized in JSON
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Monitoring endpoint
from prometheus_client import Counter, generate_latest
from flask import Response

REQUEST_COUNTER = Counter('extract_csv_requests_total', 'Total requests for the extract CSV service')
SUCCESS_COUNTER = Counter('extract_csv_success_total', 'Total successful requests for the extract CSV service')
ERROR_COUNTER = Counter('extract_csv_error_total', 'Total failed requests for the extract CSV service')

@bp.route('/metrics', methods=['GET'])
def metrics():
    """
    Prometheus monitoring endpoint.

    Returns:
    - Metrics collected by Prometheus as plaintext.
    """
    REQUEST_COUNTER.inc()  # Increment total requests
    return Response(generate_latest(), mimetype="text/plain")