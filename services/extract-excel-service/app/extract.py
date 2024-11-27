import pandas as pd
import os

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