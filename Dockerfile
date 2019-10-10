# use docker build --build-arg SSH_PRIVATE_KEY="$( cat ~/.ssh/id_rsa )" ....
FROM python:3.7

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# add credentials on build
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod -R 600 /root/.ssh

# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan gitlab.com >> /root/.ssh/known_hosts

RUN pip install poetry
RUN poetry config settings.virtualenvs.create false
RUN poetry install

RUN rm -rf /root/.ssh

EXPOSE 80

COPY config.ini config.ini

COPY ./app /app

CMD exec uvicorn app.main:app --host 0.0.0.0 --port 80
