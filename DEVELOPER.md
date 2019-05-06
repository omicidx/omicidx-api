# Developer docs

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
- http://127.0.0.1:8000/doc 

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
