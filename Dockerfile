# Use base image of python 3.9
FROM python:3.9-slim

# Setting the working directory
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the code in the working dir
COPY . .

# Expose the 5001 port -- used by the microservice
EXPOSE 5001

# Command to start the microservice
CMD ["python", "run.py"]
