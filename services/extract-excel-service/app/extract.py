import pandas as pd
import os
import pyarrow as pa
import pyarrow.ipc as pa_ipc
import logging

logger = logging.getLogger('extract-excel-service')

def arrow_to_ipc(arrow_table):
    """
    Serializes an Arrow Table to IPC format (stream).
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

def process_excel(file_path):
    """
    Carica un file Excel e lo restituisce come DataFrame.
    """
    try:
        # Verifica che l'estensione sia supportata
        ext = os.path.splitext(file_path)[-1].lower()
        if ext not in ['.xls', '.xlsx']:
            raise ValueError(f"Formato file non supportato: {ext}. Supportati: .xls, .xlsx")
        
        # Carica il file Excel in un DataFrame
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Errore durante l'elaborazione del file Excel: {str(e)}")