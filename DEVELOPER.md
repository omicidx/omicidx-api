# Developer docs

## Configuration setup

Configuration is via a `toml` file. The location of the file
is contained in the environment variable `OMICIDX_CONFIGURAITON_FILE`.

To ease development, I use a `.env` file and load it at the top of the 
main app. See [python-dotenv](https://saurabh-kumar.com/python-dotenv/) for
details.

## working with fastapi

### Run the code

Assumes the code is at `app.main:app`

- https://fastapi.tiangolo.com/tutorial/intro/#run-the-code

```
uvicorn main:app --reload
```

### openapi urls

[openapi version 3](https://github.com/swagger-api/swagger-ui)

- http://localhost:8000/openapi.json
- http://127.0.0.1:8000/redoc (see [ReDoc](https://github.com/Rebilly/ReDoc))
- http://127.0.0.1:8000/docs 

### testing

- https://fastapi.tiangolo.com/tutorial/testing/

- put tests in `tests` directory
- function files must be called `test_.....`
- functions must be called `test_....`

To run tests:

```
pip install --editable .
pytest
```

Example test file, see `tests/test_app.py`.

## docker

- Docker exposes port 80.
- **Copies** config.ini into container, *so don't expose container publicly.*

```
docker build -t seandavi/omicidx_fastapi .
docker run -p 9080:80 seandavi/omicidx_fastapi
```

## Kubernetes

### secrets

The config file contains all the secrets. 

```
kubectl create secret generic omicidx-config --from-file=../omicidx-config.toml
```

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: omicidx-fastapi
  labels:
    app: omicidx-fastapi
spec:
  replicas: 2
  selector:
    matchLabels:
      app: omicidx-fastapi
  template:
    metadata:
      labels:
        app: omicidx-fastapi
    spec:
      volumes:
        - name: omicidx-api
          secret:
            secretName: omicidx-config
      containers:
      - name: omicidx-fastapi
        image: gcr.io/isb-cgc-01-0006/omicidx-fastapi
        ports:
          - containerPort: 80
        volumeMounts:
          - name: omicidx-config
            readOnly: true
            mountPath: "/etc/omicidx-api"
		env:
		  - name: OMICIDX_CONFIG_FILE
          value: '/etc/omicidx-api/omicidx-config'

```
