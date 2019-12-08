from fastapi import (APIRouter, Depends)
from ..dependers import (GetByAccession, GetSubResource, SimpleQueryStringSearch)
import omicidx.sra.pydantic_models as p
from ..response_models import (ResponseModel, MappingResults)

from ..elastic_connection import connections

router = APIRouter()


@router.get("/study/{accession}", tags=['SRA'])
async def get_study_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_study')


@router.get("/study/{accession}/runs", tags=['SRA'])
async def get_study_runs(getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_study', 'sra_run')


@router.get("/study/{accession}/experiments", tags=['SRA'])
async def get_study_experiments(
        getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_study', 'sra_experiment')


@router.get("/study/{accession}/samples", tags=['SRA'])
async def get_study_samples(getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_study', 'sra_sample')


@router.get("/sample/{accession}", tags=['SRA'])
async def get_sample_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_sample')


@router.get("/sample/{accession}/experiments", tags=['SRA'])
async def get_sample_experiments(
        getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_sample', 'sra_experiment')


@router.get("/sample/{accession}/runs", tags=['SRA'])
async def get_sample_runs(getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_sample', 'sra_run')


@router.get("/experiment/{accession}/runs", tags=['SRA'])
async def get_experiment_runs(
        getter: GetSubResource = Depends(GetSubResource)):
    return getter.get('sra_experiment', 'sra_run')


@router.get("/run/{accession}", tags=['SRA'])
async def get_run_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_run')


@router.get("/experiment/{accession}", tags=['SRA'])
async def get_experiment_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_experiment')






@router.get("/studies/search", tags=['SRA', 'Search'], response_model=ResponseModel)
async def search_studies(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_study')


@router.get("/experiments/search", tags=['SRA', 'Search'], response_model=ResponseModel)
async def search_experiments(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_experiment')


@router.get("/runs/search", tags=['SRA', 'Search'], response_model=ResponseModel)
async def search_runs(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_run')


@router.get("/samples/search", tags=['SRA', 'Search'], response_model=ResponseModel)
async def search_samples(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_sample')


