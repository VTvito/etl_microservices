import pyarrow as pa
import pyarrow.ipc as pa_ipc
import logging

logger = logging.getLogger('clean-nan-service')

def apply_transformations(arrow_table):
    """
    Cleans the data by dropping rows with null values.

    Args:
        arrow_table (pyarrow.Table): Input Arrow Table to be cleaned.

    Returns:
        pyarrow.Table: Cleaned Arrow Table with no null values.
    """
    try:
        # Convert to Pandas for easier manipulation
        df = arrow_table.to_pandas()
        logger.info(f"Converted Arrow Table to Pandas DataFrame with {df.shape[0]} rows and {df.shape[1]} columns.")

        # Drop rows with NaN values
        df_cleaned = df.dropna()
        logger.info(f"Dropped NaN values, resulting in {df_cleaned.shape[0]} rows.")

        # Convert back to Arrow Table
        cleaned_arrow_table = pa.Table.from_pandas(df_cleaned)
        logger.info(f"Converted cleaned Pandas DataFrame back to Arrow Table with {cleaned_arrow_table.num_rows} rows.")

        return cleaned_arrow_table
    except Exception as e:
        logger.error(f"Failed to clean data: {e}")
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