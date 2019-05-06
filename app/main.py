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


@app.get("/study/{accession}")
async def get_study_accession(accession: str ):
    try:
        return es.client.get(index="sra_study", doc_type="doc", id=accession)
    except elasticsearch.exceptions.NotFoundError as e:
        raise HTTPException(
            status_code = 404,
            detail = f"Accession {accession} not found."
        )
    
@app.get("/studies/search")
async def search_study(q: str = Query(None, description = "The query, using lucene query syntax"),
                       size: int = Query(10, gte=0, lt=1000),
):
    """Search studies

    uses [lucene query string syntax](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html)
    """
    search = Search(using = es.client)
    resp = search.index('sra_study').query('query_string', query = q).execute()
    return resp[0:size]
