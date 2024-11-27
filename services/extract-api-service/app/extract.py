import pandas as pd
import requests

def extract_from_api(api_url, api_params, auth_type=None, auth_value=None):
    """
    Esegue una chiamata all'endpoint API e restituisce i dati come DataFrame.
    Supporta autenticazione tramite API key
    """
    try:
        headers = {}

        # Configura le intestazioni di autenticazione
        if auth_type == "api_key":
            headers["x-api-key"] = auth_value
        else:
            raise ValueError(f"Tipo di autenticazione '{auth_type}' non supportato")

        # Effettua la richiesta GET
        response = requests.get(api_url, params=api_params, headers=headers, timeout=30)
        response.raise_for_status()

        # Converti la risposta in un DataFrame
        data = pd.json_normalize(response.json())
        return data

    except requests.RequestException as e:
        raise ValueError(f"Errore API: {str(e)}")
