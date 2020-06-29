from fastapi import (APIRouter, Depends)
from app.dependers import (GetByAccession, GetSubResource, SimpleQueryStringSearch)
import omicidx.sra.pydantic_models as p
from app.response_models import (ResponseModel, MappingResults)
from enum import Enum

from app.elasticsearch.connection import connections
from app.elasticsearch.utils import (get_flattened_mapping_from_index)

router = APIRouter()

# TODO: belongs elsewhere
class EntityName(str, Enum):
    gse = "series"
    gsm = "sample"
    gpl = "platform"


@router.get("/fields/{entity}")
def mapping(entity: EntityName) -> dict:
    entity_string = str(entity.name)
    print(entity_string)
    return get_flattened_mapping_from_index('geo_' + entity_string)


@router.get("/series/{accession}")
async def series_by_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_study')


@router.get("/series", 
            response_model=ResponseModel)
async def search_series(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('geo_gse')


#@router.get("/series/{accession}/samples")
#async def samples_for_study(getter: GetSubResource = Depends(GetSubResource)):
#    return getter.get('geo_gse', 'sra_gsm')


@router.get("/platforms/{accession}/samples")
async def samples_for_platform(
        getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('geo_gpl', 'geo_gsm')


@router.get("/platform/{accession}", tags=['GEO Platforms'])
async def platform_by_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('geo_gpl')



@router.get("/platforms", response_model=ResponseModel)
async def search_platforms(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('geo_gpl')


@router.get("/samples/{accession}")
async def sample_by_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('geo_gsm,')


@router.get("/samples", response_model=ResponseModel)
async def search_samples(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('geo_gsm')

