from pydantic import BaseModel
from typing import List, Dict

class ResponseStats(BaseModel):
    total: int
    took: float

class Hit(dict):
    """Hit object"""
    pass

class TermFacetResult(BaseModel):
    key: str
    doc_count: int

class TermFacet(BaseModel):
    doc_count_error_upper_bound: int
    sum_other_doc_count: int
    buckets: List[TermFacetResult]
    
class ResponseModel(BaseModel):
    hits: List[Hit]
    facets: Dict[str, TermFacet]
    cursor: str = None
    stats: ResponseStats
    success: bool
