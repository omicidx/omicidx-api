from fastapi import (APIRouter, Depends)
from app.dependers import (SimpleQueryStringSearch, GetByAccession)
from app.response_models import ResponseModel
from enum import Enum
from app.elasticsearch.utils import (get_flattened_mapping_from_index)


router = APIRouter()

# TODO: may want to implement stuff for bioproject


@router.get("/fields/{entity}")
def mapping(entity: str) -> dict:
    #entity_string = str(entity.name)
    #print(entity_string)
    #return get_flattened_mapping_from_index('sra_' + entity_string)
    return get_flattened_mapping_from_index('biosample')

@router.get("/samples", tags=['Biosample'], response_model=ResponseModel)
async def biosamples(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('biosample')


# TODO: implement biosample pydandic model
@router.get("/samples/{accession}", tags=['Biosample'])
async def biosample_by_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('biosample')
