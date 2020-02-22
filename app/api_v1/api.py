from fastapi import APIRouter

from app.api_v1.endpoints import (sra, biosample)

api_router = APIRouter()

api_router.include_router(sra.router, prefix='/sra', tags=['SRA'])
api_router.include_router(biosample.router, prefix='/biosample', tags=['Biosample'])
