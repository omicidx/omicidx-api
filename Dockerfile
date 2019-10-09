FROM python:3.7

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN pip install poetry
RUN poetry config settings.virtualenvs.create false
RUN poetry install

EXPOSE $PORT

COPY config.ini config.ini

COPY ./app /app

CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
