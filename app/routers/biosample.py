from fastapi import (APIRouter, Depends)
from ..dependers import (SimpleQueryStringSearch, GetByAccession)
from ..response_models import ResponseModel

router = APIRouter()

# TODO: may want to implement stuff for bioproject


@router.get("/samples", tags=['Biosample'], response_model=ResponseModel)
async def biosamples(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('biosample')


# TODO: implement biosample pydandic model
@router.get("/samples/{accession}", tags=['Biosample'])
async def biosample_by_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('biosample')
