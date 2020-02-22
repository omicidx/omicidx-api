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
    study = "studies"
    run   = "runs"
    experiment = "experiments"
    sample     = "samples"


@router.get("/fields/{entity}")
def mapping(entity: EntityName) -> dict:
    entity_string = str(entity.name)
    print(entity_string)
    return get_flattened_mapping_from_index('sra_' + entity_string)
    return get_flattened_mapping_from_index('biosample')


@router.get("/studies/{accession}", tags=['SRA'])
async def study_by_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_study')


@router.get("/studies", tags=['SRA'], response_model=ResponseModel)
async def studies(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_study')


@router.get("/studies/{accession}/samples", tags=['SRA'])
async def samples_for_study(getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_study', 'sra_sample')


@router.get("/studies/{accession}/experiments", tags=['SRA'])
async def experiments_for_study(
        getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_study', 'sra_experiment')


@router.get("/studies/{accession}/runs", tags=['SRA'])
async def runs_for_study(getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_study', 'sra_run')


@router.get("/samples/{accession}", tags=['SRA'])
async def sample_by_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_sample')


@router.get("/samples", tags=['SRA'], response_model=ResponseModel)
async def samples(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_sample')


@router.get("/samples/{accession}/experiments", tags=['SRA'])
async def experiments_for_sample(
        getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_sample', 'sra_experiment')


@router.get("/samples/{accession}/runs", tags=['SRA'])
async def runs_for_sample(getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_sample', 'sra_run')


@router.get("/experiments/{accession}", tags=['SRA'])
async def experiment_by_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_experiment')


@router.get("/experiments", tags=['SRA'], response_model=ResponseModel)
async def experiments(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_experiment')


@router.get("/experiments/{accession}/runs", tags=['SRA'])
async def runs_for_experiment(
        getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_experiment', 'sra_run')


@router.get("/runs/{accession}", tags=['SRA'])
async def run_by_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_run')


@router.get("/runs", tags=['SRA'], response_model=ResponseModel)
async def runs(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_run')




