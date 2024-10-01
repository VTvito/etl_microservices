import pandas as pd

def load_csv(file_path):
    """
    Function that load data from CSV file
    """
    return pd.read_csv(file_path)
