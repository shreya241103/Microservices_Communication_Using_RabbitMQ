# Use the official Python image
FROM python:3.9-slim

WORKDIR /app

COPY main.py .
COPY ddl.py .
COPY crud.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
