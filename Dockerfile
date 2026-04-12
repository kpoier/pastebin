FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the uploads directory exists
RUN mkdir -p uploads && chmod 777 uploads

# Create an empty db file to prevent directory projection by Docker volumes
RUN touch database.db && chmod 666 database.db

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
