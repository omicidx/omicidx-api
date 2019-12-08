from fastapi import (APIRouter, Depends)
from ..dependers import (SimpleQueryStringSearch, GetByAccession)
from ..response_models import ResponseModel

router = APIRouter()

# TODO: may want to implement stuff for bioproject


@router.get("/sample/search", tags=['Biosample', 'Search'], response_model=ResponseModel)
async def search_biosamples(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('biosample')


# TODO: implement biosample pydandic model
@router.get("/sample/{accession}", tags=['Biosample'])
async def get_biosample_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('biosample')
