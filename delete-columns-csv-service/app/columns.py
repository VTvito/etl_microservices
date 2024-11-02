import pandas as pd

def delete_columns_from_csv(file_path, columns):
    """
    Rimuove le colonne specificate da un CSV e restituisce il percorso del file aggiornato.
    """
    df = pd.read_csv(file_path)
    df.drop(columns=columns, inplace=True, errors='ignore')
    df.to_csv(file_path, index=False)
    return file_path