# use docker build --build-arg SSH_PRIVATE_KEY="$( cat ~/.ssh/id_rsa )" ....
FROM python:3.7

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN pip install poetry
RUN poetry config settings.virtualenvs.create false
RUN poetry install --no-dev -n

RUN rm -rf /root/.ssh

EXPOSE 80

COPY . .

# mount with -v PATH/TO/:/etc/omicidx
ENV OMICIDX_CONFIGURATION_FILE=/etc/omicidx/omicidx-config.toml

CMD exec uvicorn app.main:app --host 0.0.0.0 --port 80
