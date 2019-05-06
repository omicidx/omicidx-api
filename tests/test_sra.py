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
