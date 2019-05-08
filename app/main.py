from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    Depends,
    Path
)
from pydantic import (
    BaseModel,
    ValidationError,
    validator,
    Schema
)
from typing import List, Any
from .esclient import ESClient
from elasticsearch_dsl import Search
import elasticsearch

app = FastAPI(title='OmicIDX', version='1.0')

es = ESClient('config.ini')

@app.get("/")
async def root():
    return {"message": "Hello World"}



class GetByAccession():
    def __init__(self,
                 accession: str = Path(
                     ...,
                     description = "An accession for lookup"
                 )):
        self.accession = accession

    def get(self, index, doc_type="doc"):
        try:
            return es.client.get(index=index, doc_type=doc_type, id=self.accession)
        except elasticsearch.exceptions.NotFoundError as e:
            raise HTTPException(
                status_code = 404,
                detail = f"Accession {self.accession} not found in index {index}."
            )
        

@app.get("/study/{accession}", tags=['SRA'])
async def get_study_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_study')

@app.get("/sample/{accession}", tags=['SRA'])
async def get_sample_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_sample')

@app.get("/experiment/{accession}", tags=['SRA'])
async def get_experiment_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_experiment')

@app.get("/run/{accession}", tags=['SRA'])
async def get_run_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_run')



class SimpleQueryStringSearch():
    def __init__(self,
                 q: str = Query(
                     None,
                     description = "The query, using lucene query syntax",
                     example = "cancer AND breast AND published:[2018 TO 2021]"),
                 size: int = Query(10, gte = 0, lt = 1000, example = 10),
                 facets: List[str] = Query(
                     [],
                     description = ('A list of strings identifying fields '
                                    'for faceted search results. Simple '
                                    'term faceting is used here, meaning '
                                    'that fields that are short text and repeated '
                                    'across records will be binned and counted.'),
                     example = ['center_name.keyword'],
                     )
    ):
        self.q = q
        self.size = size
        self.facets = facets

    def search(self, index):
        search = Search(using = es.client)
        s = search.index(index).query('query_string', query = self.q)
        for agg in self.facets:
            # these update the s object in place
            # as opposed to the query method(s) that
            # return a new copied object
            s.aggs.bucket(agg,'terms',field=agg)
        resp = s.execute()
        return {"hits": [res for res in resp[0:self.size]],
                "facets": resp.aggs.to_dict()}

    
@app.get("/studies/search", tags=['SRA', 'Search'])
async def search_studies(searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_study')

@app.get("/experiments/search", tags=['SRA', 'Search'])
async def search_experiments(searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_experiment')

@app.get("/runs/search", tags=['SRA', 'Search'])
async def search_runs(searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_run')

@app.get("/samples/search", tags=['SRA', 'Search'])
async def search_samples(searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_sample')




@app.get("/sql", tags=["SQL"])
async def elasticsearch_sql(
        query: str = Query(...,
                           example = "SELECT * FROM sra_study WHERE QUERY('breast cancer')",
                           description = ('And Elasticsearch SQL query. See the '
                                          'endpoint description for more details.'),
        ),
        cursor: str = Query(None,
                            description = ('The cursor returned by a large result '
                                           'set can be used here to fetch the next '
                                           'set of results.'),),
        size: int = Query(500, gte=0, lt=1000, example = 10,
                          description = ('The size of the result set to return. '
                                         'Minimum: 0, maximum: 1000. Use the '
                                         '`cursor` functionality to loop over result '
                                         'sets larger than `size`.'),
                          )
):
    """Use Elasticsearch SQL to get results.

    Elasticsearch SQL has some limitations relative to regular relational
    databases, but it can still be useful. In particular, there are no
    "joins" available in Elasticsearch SQL.

    See: 
      - [elasticsearch SQL documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-syntax-select.html)
      - [An Introduction to Elasticsearch SQL with Practical Examples - Part 1](https://www.elastic.co/blog/an-introduction-to-elasticsearch-sql-with-practical-examples-part-1)
      - [An Introduction to Elasticsearch SQL with Practical Examples - Part 2](https://www.elastic.co/blog/an-introduction-to-elasticsearch-sql-with-practical-examples-part-2)
      - [Elasticsearch functions and operators](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions.html)

    ## Example queries

    These example queries can be pasted into the `query` field on 
    the online docs or can be used in the `query` field from a
    client. Note that it may be beneficial to change the default
    `size` field to a larger value (up to the maximum). For `GROUP BY`
    queries, there is an intrinsic limit of 512 records, so specifying
    `LIMIT` greater than 512 will result in errors.

    Select all top-level fields from sra studies. Note that the
    result will include a `cursor` field. Supply the `cursor` string
    to the cursor field and rerun the query to get the next batch
    of results.

    ```
    select * from sra_study
    ```

    Get a count of the visibility (open, controlled access, etc.) from all studies.

    ```
    select visibility, count(*) 
    from sra_study 
    group by visibility
    ```
    
    Get a count of the number of studies publised by month.

    ```
    select MONTH(published) as month,
           YEAR(published) as year,
           count(*)
    from sra_study 
    group by month, year
    order by year desc, month desc
    ```
    Perform a full text search on experiments and get a count of records.

    ```
    select count(*) as experiment_count
    from sra_experiment
    where QUERY('cancer')
    ```

    And get a count of the library_strategies associated with those
    experiments.

    ```
    select count(*) as experiment_count, library_strategy
    from sra_experiment
    where QUERY('cancer')
    group by library_strategy
    order by experiment_count desc
    limit 100
    ```

    """
    try:
        if(cursor is not None):
            return es.client.transport.perform_request('POST','/_xpack/sql',body={"cursor":cursor})
        return es.client.transport.perform_request('POST','/_xpack/sql',body={
            "query":query,
            "fetch_size": size
        })
            
    except elasticsearch.exceptions.TransportError as e:
        return e.info['error'], 400


class ExtendedSearch(BaseModel):
    """This encapsulates all the pieces of an 
    extendedQuery. The only required field is 
    the `query` field.
    """
    query: dict = Schema(...)
    aggs: dict = Schema(
        {},
        description = "Aggregates"
    )
    size: int = Schema(
        10,
        description = ('The maximum number of records to return'),
        gte = 0,
        lte = 1000
    )
    filter: dict = Schema(
        {},
        description = "Filters"
    )
    search_after: List[Any] = Schema(
        [],
        description = "search_after functionality"
    )
    sort: List[dict] = Schema(
        [{}],
        description = "sort by"
    )

    @validator('size')
    def check_size(cls, v):
        if(v<0 or v>1000):
            raise ValueError(f'size {v} must be between 0 and 1000. '
                             'For large result sets, use search_after '
                             'and cursor functionality.' 
            )
        return v

    def do_search(self, index):
        """do a full elasticsearch search

        index: str 
            the elasticsearch index

        returns the raw elasticsearch response.
        """
        body_dict = self.dict()
        
        # need to clean up defaults
        if(len(body_dict['aggs'])==0):
            del(body_dict['aggs'])

        if(len(body_dict['search_after'])==0):
            del(body_dict['search_after'])

        if(len(body_dict['sort'])==1):
            if(len(body_dict['sort'][0])==0):
                del(body_dict['sort'])

        if(len(body_dict['filter'])==0):
            del(body_dict['filter'])

        # and perform the search
        resp = es.client.search(index = index, body=body_dict)

        # returns raw elasticsearch response
        return resp


    
@app.post("/studies/extendedSearch")
def extended_study_search(
        body: ExtendedSearch
):
    return body.do_search('sra_study')

@app.post("/samples/extendedSearch")
def extended_samples_search(
        body: ExtendedSearch
):
    return body.do_search('sra_sample')

@app.post("/experiments/extendedSearch")
def extended_experiment_search(
        body: ExtendedSearch
):
    return body.do_search('sra_experiment')

@app.post("/runs/extendedSearch")
def extended_study_search(
        body: ExtendedSearch
):
    return body.do_search('sra_run')
