FROM python:3.12-slim

WORKDIR /app

# Сначала зависимости — чтобы слой кэшировался и не пересобирался при правках кода
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50051

CMD ["python", "server.py"]
