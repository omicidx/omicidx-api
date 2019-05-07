from fastapi import (FastAPI,
                     HTTPException,
                     Query,
                     Depends
                     )
from pydantic import BaseModel, ValidationError, validator
from .esclient import ESClient
from elasticsearch_dsl import Search
import elasticsearch

app = FastAPI(title='OmicIDX', version='1.0')

es = ESClient('config.ini')

@app.get("/")
async def root():
    return {"message": "Hello World"}




@app.get("/study/{accession}", tags=['SRA study', 'SRA'])
async def get_study_accession(accession: str ):
    try:
        return es.client.get(index="sra_study", doc_type="doc", id=accession)
    except elasticsearch.exceptions.NotFoundError as e:
        raise HTTPException(
            status_code = 404,
            detail = f"Accession {accession} not found."
        )



class CommonQueryParams:
    def __init__(self,
                 q: str = Query(
                     None,
                     description = "The query, using lucene query syntax",
                     example = "cancer AND breast AND published:[2018 TO 2021]"),
                 size: int = Query(10, gte = 0, lt = 1000, example = 10)):
        self.q = q
        self.size = size

    def search(self, index):
        search = Search(using = es.client)
        resp = search.index(index).query('query_string', query = self.q).execute()
        return resp[0:self.size]

    
@app.get("/studies/search", tags=['SRA', 'Search'])
async def search_study(searcher: CommonQueryParams = Depends(CommonQueryParams)):
    return searcher.search('sra_study')

@app.get("/experiments/search", tags=['SRA', 'Search'])
async def search_study(searcher: CommonQueryParams = Depends(CommonQueryParams)):
    return searcher.search('sra_experiment')

@app.get("/runs/search", tags=['SRA', 'Search'])
async def search_study(searcher: CommonQueryParams = Depends(CommonQueryParams)):
    return searcher.search('sra_run')

@app.get("/samples/search", tags=['SRA', 'Search'])
async def search_study(searcher: CommonQueryParams = Depends(CommonQueryParams)):
    return searcher.search('sra_sample')




@app.get("/sql", tags=["SQL"])
async def elasticsearch_sql(query: str = Query(..., example = "SELECT * FROM sra_study WHERE QUERY('breast cancer')"),
                            cursor: str = None,
                            size: int = Query(500, gte=0, lt=1000, example = 10),
):
    """Use elasticsearch sql to get results

    See: 
      - [elasticsearch SQL documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-syntax-select.html)
      - [An Introduction to Elasticsearch SQL with Practical Examples - Part 1](https://www.elastic.co/blog/an-introduction-to-elasticsearch-sql-with-practical-examples-part-1)
      - [An Introduction to Elasticsearch SQL with Practical Examples - Part 2](https://www.elastic.co/blog/an-introduction-to-elasticsearch-sql-with-practical-examples-part-2)
      - [Elasticsearch functions and operators](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions.html)
    """
    try:
        if(cursor is not None):
            return es.client.transport.perform_request('POST','/_xpack/sql',body={"cursor":cursor})
        return es.client.transport.perform_request('POST','/_xpack/sql',body={
            "query":query,
            "fetch_size": size
        })
            
    except elasticsearch.exceptions.TransportError as e:
        return e.info['error'], 400


class FullQuery(BaseModel):
    query: dict
    aggs: dict = None
    size: int = 10

    @validator('size')
    def check_size(cls, v):
        if(v<0 or v>1000):
            raise ValueError(f'size {v} is not between 0 and 1000')
        return v

    
@app.post("/studies/search/")
def post_full_es_json(body: FullQuery
):
    """Allow full ElasticSearch json

    body : json
        The full json string passed unchanged to elasticsearch
    
    Returns
    -------
    The response from elasticsearch, unchanged
    """
    entity='study'
    query_body = {"query":body.query}
    if(body.aggs is not None):
        query_body.update({"aggs":body.aggs})
    resp = es.client.search(index = 'sra_{}'.format(entity), body=query_body, size=body.size)
    return resp
