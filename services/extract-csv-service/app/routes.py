from flask import Blueprint, jsonify, request, Response
from app.read import load_csv_to_arrow, arrow_to_ipc
import pyarrow as pa
import pyarrow.ipc as pa_ipc
from prometheus_client import Counter, generate_latest

bp = Blueprint('extract-csv', __name__)

# Monitoring counters
REQUEST_COUNTER = Counter('clean_nan_requests_total', 'Total requests for the clean NaN service')
SUCCESS_COUNTER = Counter('clean_nan_success_total', 'Total successful requests for the clean NaN service')
ERROR_COUNTER = Counter('clean_nan_error_total', 'Total failed requests for the clean NaN service')

@bp.route('/extract-csv', methods=['POST'])
def extract_csv():
    """
    API Endpoint to extract data from a CSV file and serialize it into Apache Arrow IPC format.

    Request Body:
    - client_id (str): ID of the client requesting the operation.
    - file_path (str): Path to the input CSV file.

    Returns:
    - Response containing Arrow IPC serialized data.
    """
    try:
        REQUEST_COUNTER.inc()

        file_path = request.json.get('file_path')
        if not file_path:
            return jsonify({"error": "Parameter 'file_path' is required"}), 400

        # Load CSV into Arrow Table
        arrow_table = load_csv_to_arrow(file_path)

        # Serialize Arrow Table to IPC format
        ipc_data = arrow_to_ipc(arrow_table)

        SUCCESS_COUNTER.inc()
        return Response(ipc_data, content_type="application/vnd.apache.arrow.stream"), 200

    except Exception as e:
        ERROR_COUNTER.inc()
        return jsonify({"status": "error", "message": str(e)}), 500
    

@bp.route('/metrics', methods=['GET'])
def metrics():
    """
    Prometheus monitoring endpoint.

    Returns:
    - Metrics collected by Prometheus as plaintext.
    """
    return Response(generate_latest(), mimetype="text/plain")