FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    sqlite3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "banco.py"]