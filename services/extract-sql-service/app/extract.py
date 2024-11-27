from sqlalchemy import create_engine
import pandas as pd

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