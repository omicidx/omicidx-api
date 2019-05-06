from starlette.testclient import TestClient
import app.main as main

app = main.app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    

