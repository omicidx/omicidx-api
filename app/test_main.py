from fastapi import FastAPI
from starlette.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def _get_accession(entity, accession):
    response = client.get("/{}/{}".format(entity, accession))
    assert response.status_code == 200
    json = response.json()
    assert json['accession'] == accession
    
    
def test_get_study_accession():
    _get_accession("study", "SRP006387")

def test_get_run_accession():
    _get_accession("run", "SRR6077637")

def test_get_experiment_accession():
    _get_accession("experiment", "SRX1602907")
    
def test_get_sample_accession():
    _get_accession("sample", "SRS421036")


    
