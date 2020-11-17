FROM python:3.8-slim

RUN apt-get update \
    && apt-get install -y gdal-bin libgdal-dev python3-gdal python-psycopg2

COPY ./app/ /app/
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip; pip install -r /app/requirements.txt

ENV PYTHONIOENCODING=utf-8 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    SETTINGS_FILE_FOR_DYNACONF=core.settings

WORKDIR /app
ENTRYPOINT ["sh", "/app/entrypoint.sh"]

# execute the app
CMD ["/usr/local/bin/gunicorn", "app:application", "-n", "task", "-w", "1", "-b", "0.0.0.0:8000"]