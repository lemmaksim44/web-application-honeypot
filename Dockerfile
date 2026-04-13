FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y gcc netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY admin_honeypot/ /usr/local/lib/python3.12/site-packages/admin_honeypot/

COPY app /app

COPY app/static/ /app/static/
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
