from flask import Blueprint, jsonify, request, Response
from app.clean import apply_transformations
import pyarrow as pa
import pyarrow.ipc as pa_ipc
from prometheus_client import Counter, generate_latest

bp = Blueprint('clean-nan', __name__)

# Monitoring counters
REQUEST_COUNTER = Counter('clean_nan_requests_total', 'Total requests for the clean NaN service')
SUCCESS_COUNTER = Counter('clean_nan_success_total', 'Total successful requests for the clean NaN service')
ERROR_COUNTER = Counter('clean_nan_error_total', 'Total failed requests for the clean NaN service')

@bp.route('/clean-nan', methods=['POST'])
def clean_nan():
    """
    API Endpoint to clean data by removing NaN values.
    
    Request Body:
    - Arrow IPC data in binary format.
    
    Returns:
    - Cleaned data in Arrow IPC binary format.
    """
    try:
        REQUEST_COUNTER.inc()

        # Ottieni i dati binari dal corpo della richiesta
        arrow_ipc = request.get_data()
        if not arrow_ipc:
            return jsonify({"error": "No data received"}), 400

        # Deserializza la Tabella Arrow dal formato IPC
        try:
            reader = pa_ipc.open_stream(pa.BufferReader(arrow_ipc))
            arrow_table = reader.read_all()
        except Exception as e:
            return jsonify({"error": f"Failed to parse Arrow IPC data: {str(e)}"}), 400

        # Applica le trasformazioni
        cleaned_arrow_table = apply_transformations(arrow_table)

        # Serializza la Tabella Arrow pulita in formato IPC
        try:
            sink = pa.BufferOutputStream()
            with pa_ipc.new_stream(sink, cleaned_arrow_table.schema) as writer:
                writer.write_table(cleaned_arrow_table)
            cleaned_arrow_ipc = sink.getvalue().to_pybytes()
        except Exception as e:
            raise ValueError(f"Failed to serialize cleaned Arrow Table to IPC: {e}")

        SUCCESS_COUNTER.inc()
        return Response(
            cleaned_arrow_ipc,
            status=200,
            mimetype='application/vnd.apache.arrow.stream'
        )

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