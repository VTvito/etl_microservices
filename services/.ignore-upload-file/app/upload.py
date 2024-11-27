import os

DATA_FOLDER = '/app/data'

def save_uploaded_file(file, client_id, dataset_name):
    """
    Salva il file caricato nella cartella specificata per il cliente e dataset.
    """
    # Crea la directory del cliente se non esiste già
    client_folder = os.path.join(DATA_FOLDER, client_id)
    os.makedirs(client_folder, exist_ok=True)

    # Salva il file nella directory specifica
    file_path = os.path.join(client_folder, dataset_name)
    file.save(file_path)

    return file_path