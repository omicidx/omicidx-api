from starlette.testclient import TestClient

from ..main import app

client = TestClient(app)

def search_endpoint(endpoint, q, size=10):
    response = client.get(f"/{endpoint}/search", params = {"q": q, "size": size})
    assert response.status_code == 200
    json = response.json()
    return json


def test_search_study():
    retval = search_endpoint('studies',q='cancer AND published:[2018-01-01 TO *]')
    assert len(retval['hits']) > 0
    assert retval['cursor'] is not None


def test_search_run():
    retval = search_endpoint('runs',q='published:[2018-01-01 TO *]')
    assert len(retval['hits']) > 0
    assert retval['cursor'] is not None


def test_search_sample():
    retval = search_endpoint('samples',q='cancer AND published:[2018-01-01 TO *]')
    assert len(retval['hits']) > 0
    assert retval['cursor'] is not None


def test_search_experiment():
    retval = search_endpoint('experiments',q='cancer AND published:[2018-01-01 TO *]')
    assert len(retval['hits']) > 0
    assert retval['cursor'] is not None


def test_search_size_zero():
    """Test behavior of search when size=0"""
    retval = search_endpoint('experiments',q='cancer AND published:[2018-01-01 TO *]', size=0)
    assert len(retval['hits'])==0
    # when size=0, assume that no records are meant to
    # be returned, so no cursor created.
    assert retval['cursor'] is None


