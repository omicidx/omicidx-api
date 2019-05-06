from fastapi import FastAPI
from .esclient import ESClient

app = FastAPI()

es = ESClient('config.ini')

@app.get("/")
async def root():
    return {"message": "Hello World"}


