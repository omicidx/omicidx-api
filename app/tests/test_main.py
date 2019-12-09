import pytest
import os
from fastapi import FastAPI
from starlette.testclient import TestClient

if not os.getenv('OMICIDX_CONFIGURATION_FILE', False):
    pytest.skip("skipping tests relying on config", allow_module_level=True)

from ..main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def _get_accession(entity, accession):
    response = client.get("/sra/{}/{}".format(entity, accession))
    assert response.status_code == 200
    json = response.json()
    assert json['accession'] == accession
    
    
def test_get_study_accession():
    _get_accession("studies", "SRP006387")

def test_get_run_accession():
    _get_accession("runs", "SRR6077637")

def test_get_experiment_accession():
    _get_accession("experiments", "SRX1602907")
    
def test_get_sample_accession():
    _get_accession("samples", "SRS421036")


    
