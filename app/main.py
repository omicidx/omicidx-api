from fastapi import FastAPI, HTTPException
from fastapi import Query
from .esclient import ESClient
from elasticsearch_dsl import Search
import elasticsearch

app = FastAPI()

es = ESClient('config.ini')

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/study/{accession}")
async def get_study_accession(accession: str):
    try:
        return es.client.get(index="sra_study", doc_type="doc", id=accession)
    except elasticsearch.exceptions.NotFoundError as e:
        raise HTTPException(
            status_code = 404,
            detail = f"Accession {accession} not found."
        )
    
