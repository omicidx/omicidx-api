from starlette.testclient import TestClient
import app.main as main

app = main.app

client = TestClient(app)

def test_get_study():
    response = client.get("/study/SRP000001")
    assert response.status_code == 200
    assert response.json()['_id'] == "SRP000001"

def test_get_study():
    response = client.get("/study/SRP000001")
    assert response.status_code == 200
    assert response.json()['_id'] == "SRP000001"

def test_nonexistent_study():
    response = client.get("/study/nonexistent_study")
    assert response.status_code == 404
    assert response.json() == {"detail": "Accession nonexistent_study not found."}

def test_studies_search_works():
    response = client.get("/studies/search?q=cancer&size=5")
    assert response.status_code == 200
    assert len(response.json()['_l_']) == 5

def test_studies_search_limit_size():
    response = client.get("/studies/search?q=cancer&size=10000")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {
                    "limit_value": 1000
                },
                "loc": [
                    "query",
                    "size"
                ],
                "msg": "ensure this value is less than 1000",
                "type": "value_error.number.not_lt"
            }
        ]
    }
