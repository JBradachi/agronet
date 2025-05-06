FROM python:3.10-slim

WORKDIR /app

COPY listener.py .
COPY connection.py .

EXPOSE 5000

CMD ["python", "listener.py"]