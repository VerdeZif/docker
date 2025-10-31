FROM python:3.11-slim

# Evitar buffer en logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app
ENV DJANGO_SETTINGS_MODULE=app.settings

# Instalar dependencias del sistema (psycopg2 y Pillow suelen necesitar libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
