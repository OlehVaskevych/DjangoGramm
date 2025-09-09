#!/bin/bash
echo "Running post-deployment script..."

# Активація віртуального середовища, якщо потрібно
if [ -d "antenv" ]; then
    source antenv/bin/activate
fi

# Встановлення бібліотек
pip install --no-cache-dir -r requirements.txt

# Збір статичних файлів
python manage.py collectstatic --noinput

echo "Post-deployment script completed."

gunicorn --workers=3 --bind=0.0.0.0:$PORT myproject.wsgi