FROM python:3.7

COPY requirements-dev.txt requirements-dev.txt

RUN pip install -r requirements-dev.txt

EXPOSE 80

COPY config.ini config.ini

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
