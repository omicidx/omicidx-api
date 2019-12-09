import os
import pytest
from starlette.testclient import TestClient

if not os.getenv('OMICIDX_CONFIGURATION_FILE', False):
    pytest.skip("skipping tests relying on config", allow_module_level=True)

from ..main import app

client = TestClient(app)

host = 'http://localhost:8000/'
STUDY_ACCESSION = 'SRP002730'
EXPERIMENT_ACCESSION = 'SRX000273'
RUN_ACCESSION = 'SRR000273'
SAMPLE_ACCESSION = 'SRS000273'

def get_endpoint(entity, accession):
    response = client.get("/sra/{}/{}".format(entity, accession))
    assert response.status_code == 200
    json = response.json()
    assert json['accession'] == accession


def test_get_study():
    get_endpoint('studies',STUDY_ACCESSION)


def test_get_experiment():
    get_endpoint('experiments',EXPERIMENT_ACCESSION)


def test_get_run():
    get_endpoint('runs',RUN_ACCESSION)


def test_get_sample():
    get_endpoint('samples',SAMPLE_ACCESSION)
    
