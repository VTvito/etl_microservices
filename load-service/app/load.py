import os
import pandas as pd

DATA_FOLDER = '/app/data/loaded'

def save_data(data):
    """
    Salva i dati trasformati in un file CSV nella cartella specificata.
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    
    df = pd.DataFrame(data)
    file_path = os.path.join(DATA_FOLDER, 'loaded_data.csv')
    df.to_csv(file_path, index=False)
    
    return file_path