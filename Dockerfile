FROM python:3.11-slim-bookworm

WORKDIR /app

COPY app/app.py ./app.py

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
