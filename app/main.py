from fastapi import (FastAPI,
                     HTTPException,
                     Query,
                     )
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
    
@app.get("/studies/search", tags=['SRA Study', 'SRA', 'Search'])
async def search_study(q: str = Query(None,
                                      description = "The query, using lucene query syntax",
                                      example = "cancer AND breast AND published:[2018 TO 2021]"),
                       size: int = Query(10, gte = 0, lt = 1000, example = 10),
):
    """Search studies

    uses [lucene query string syntax](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html)
    """
    search = Search(using = es.client)
    resp = search.index('sra_study').query('query_string', query = q).execute()
    return resp[0:size]

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
