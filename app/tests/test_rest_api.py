import requests
import pytest

host = 'http://localhost:8000/'
STUDY_ACCESSION = 'SRP002730'
EXPERIMENT_ACCESSION = 'SRX000273'
RUN_ACCESSION = 'SRR000273'
SAMPLE_ACCESSION = 'SRS000273'


def get_endpoint(endpoint, id):
    url = host + f'{endpoint}/{id}'
    res = requests.get(url)
    assert(res.status_code == 200)
    assert(isinstance(res.json(), dict))
    retval = res.json()
    assert(retval['accession'] == id)


def test_get_study():
    get_endpoint('study',STUDY_ACCESSION)


def test_get_experiment():
    get_endpoint('experiment',EXPERIMENT_ACCESSION)


def test_get_run():
    get_endpoint('run',RUN_ACCESSION)


def test_get_sample():
    get_endpoint('sample',SAMPLE_ACCESSION)
    
