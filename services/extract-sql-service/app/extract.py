from sqlalchemy import create_engine
import pandas as pd
import pyarrow as pa
import pyarrow.ipc as pa_ipc
import logging

logger = logging.getLogger('extract-sql-service')

def arrow_to_ipc(arrow_table):
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

def extract_from_sql(db_url, query):
    """
    Esegue una query SQL utilizzando SQLAlchemy e restituisce i dati come DataFrame.
    """
    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            data = pd.read_sql(query, connection)
        return data
    except Exception as e:
        raise ConnectionError(f"Errore durante l'esecuzione della query: {e}")