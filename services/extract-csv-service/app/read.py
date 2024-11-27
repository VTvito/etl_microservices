import pyarrow as pa
import pyarrow.csv as pacsv
import pandas as pd

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

def arrow_to_json(arrow_table):
    """
    Converts an Arrow Table into a JSON-serializable string.

    Args:
        arrow_table (pyarrow.Table): Table containing the data.

    Returns:
        str: JSON representation of the Arrow Table.
    """
    try:
        pandas_df = arrow_table.to_pandas()
        return pandas_df.to_json(orient="records")
    except Exception as e:
        raise ValueError(f"Failed to serialize Arrow Table to JSON: {e}")
