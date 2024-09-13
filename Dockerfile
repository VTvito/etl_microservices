# Usa l'immagine base Python 3.9
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt e installa le dipendenze
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia tutto il codice sorgente nella directory di lavoro
COPY . .

# Esponi la porta 5001, che è quella usata dal microservizio Flask
EXPOSE 5001

# Comando per avviare il microservizio
CMD ["python", "run.py"]
