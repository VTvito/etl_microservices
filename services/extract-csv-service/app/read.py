import pyarrow.csv as pacsv
import pyarrow as pa
import pyarrow.ipc as pa_ipc
import logging

logger = logging.getLogger('extract-csv-service')

def load_csv_to_arrow(file_path):
    """
    Reads a CSV file and converts it into an Apache Arrow Table.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pyarrow.Table: Table containing the CSV data in Arrow format.
    """
    try:
        table = pacsv.read_csv(file_path)
        logger.info(f"Loaded CSV file {file_path} into Arrow Table with {table.num_rows} rows.")
        return table
    except Exception as e:
        logger.error(f"Failed to load CSV into Arrow format: {e}")
        raise

def arrow_to_ipc(arrow_table):
    """
    Serializes an Arrow Table to IPC format (stream).
    
    Args:
        arrow_table (pyarrow.Table): Table to serialize.
    
    Returns:
        bytes: Serialized Arrow Table in IPC format.
    """
    try:
        sink = pa.BufferOutputStream()
        with pa_ipc.new_stream(sink, arrow_table.schema) as writer:
            writer.write_table(arrow_table)
        ipc_bytes = sink.getvalue().to_pybytes()
        logger.info(f"Serialized Arrow Table to IPC format, {len(ipc_bytes)} bytes.")
        return ipc_bytes
    except Exception as e:
        logger.error(f"Failed to serialize Arrow Table to IPC format: {e}")
        raise