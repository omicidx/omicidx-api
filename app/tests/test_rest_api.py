from starlette.testclient import TestClient

from ..main import app

client = TestClient(app)

host = 'http://localhost:8000/'
STUDY_ACCESSION = 'SRP002730'
EXPERIMENT_ACCESSION = 'SRX000273'
RUN_ACCESSION = 'SRR000273'
SAMPLE_ACCESSION = 'SRS000273'

def get_endpoint(entity, accession):
    response = client.get("/{}/{}".format(entity, accession))
    assert response.status_code == 200
    json = response.json()
    assert json['accession'] == accession


def test_get_study():
    get_endpoint('study',STUDY_ACCESSION)


def test_get_experiment():
    get_endpoint('experiment',EXPERIMENT_ACCESSION)


def test_get_run():
    get_endpoint('run',RUN_ACCESSION)


def test_get_sample():
    get_endpoint('sample',SAMPLE_ACCESSION)
    
