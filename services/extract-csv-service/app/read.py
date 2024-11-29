import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.ipc as pa_ipc

def load_csv_to_arrow(file_path):
    """
    Reads a CSV file and converts it into an Apache Arrow Table.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pyarrow.Table: Table containing the CSV data in Arrow format.
    """
    try:
        return pacsv.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Failed to load CSV into Arrow format: {e}")

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
        return sink.getvalue().to_pybytes()
    except Exception as e:
        raise ValueError(f"Failed to serialize Arrow Table to IPC format: {e}")