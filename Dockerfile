FROM python:3.7

COPY requirements-dev.txt requirements-dev.txt

RUN pip install -r requirements-dev.txt

EXPOSE $PORT

COPY config.ini config.ini

COPY ./app /app

CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
