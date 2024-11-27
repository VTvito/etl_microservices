# Use base image of python 3.9
FROM python:3.9-slim

# Setting the working directory
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code in the working dir
COPY . .

# Expose the 5007 port -- this microservice used this port
EXPOSE 5007

# Command to start the microservice
CMD ["python", "run.py"]