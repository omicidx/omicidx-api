from fastapi import (APIRouter, Depends)
from ..dependers import (GetByAccession, GetSubResource, SimpleQueryStringSearch)
import omicidx.sra.pydantic_models as p
from ..response_models import (ResponseModel, MappingResults)

from ..elastic_connection import connections

router = APIRouter()


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




