FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]