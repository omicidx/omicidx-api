from starlette.testclient import TestClient
import app.main as main
import pytest

app = main.app

client = TestClient(app)

def test_get_study():
    response = client.get("/study/SRP000001")
    assert response.status_code == 200
    assert response.json()['_id'] == "SRP000001"

@pytest.mark.skip(reason="no way of currently testing this")
def test_get_sample():
    response = client.get("/sample/SRS1905109")
    assert response.status_code == 200
    assert response.json()['_id'] == "SRS1905109"

def test_get_run():
    response = client.get("/run/DRR001524")
    assert response.status_code == 200
    assert response.json()['_id'] == "DRR001524"

def test_get_experiment():
    response = client.get("/experiment/SRX000237")
    assert response.status_code == 200
    assert response.json()['_id'] == "SRX000237"

def test_get_study():
    response = client.get("/study/SRP000001")
    assert response.status_code == 200
    assert response.json()['_id'] == "SRP000001"

def test_nonexistent_study():
    response = client.get("/study/nonexistent_study")
    assert response.status_code == 404
    assert response.json() == {"detail": "Accession nonexistent_study not found in index sra_study."}

def test_studies_search_works():
    response = client.get("/studies/search?q=cancer&size=5")
    assert response.status_code == 200
    assert len(response.json()['hits']) == 5

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
