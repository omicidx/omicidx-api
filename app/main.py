from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from fastapi import (FastAPI, HTTPException, Query, Depends, Path)
from pydantic import (BaseModel, ValidationError, validator, Schema)
from starlette.responses import RedirectResponse
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.graphql import GraphQLApp
from typing import List, Any
from elasticsearch_dsl import Search, Index
import elasticsearch

from .response_models import ResponseModel
from .elastic_connection import connections
from .elastic_utils import (get_mapping_properties, get_flattened_mapping_from_index)

#from .schema import schema

# REST API models
import omicidx.sra.pydantic_models as p

from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title='OmicIDX',
              version='0.99',
              description="""

The OmicIDX API documentation is available in two forms:

- [OpenAPI/Swagger Interactive](/docs)
- [ReDoc (more readable in some ways)](/redoc)

""")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#from .schema.schema import schema
#app.add_route('/graphql', GraphQLApp(schema=schema))


# for now, redirect to the docs directly
@app.route("/")
async def home(request: Request):
    return RedirectResponse(url='/docs')


class GetByAccession():
    def __init__(self,
                 accession: str = Path(...,
                                       description="An accession for lookup")):
        self.accession = accession

    def get(self, index, doc_type="_doc"):
        try:
            return connections.get_connection().get(
                index=index,
                doc_type=doc_type,
                id=self.accession
            )['_source']
        except elasticsearch.exceptions.NotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail=f"Accession {self.accession} not found in index {index}."
            )


@app.get("/study/{accession}", tags=['SRA'], response_model=p.SraStudy)
async def get_study_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_study')


@app.get("/sample/{accession}", tags=['SRA'], response_model=p.SraSample)
async def get_sample_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_sample')


@app.get("/run/{accession}", tags=['SRA'], response_model=p.SraRun)
async def get_run_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_run')


# TODO: implement biosample pydandic model
@app.get("/biosample/{accession}", tags=['Biosample'] )
async def get_biosample_accession(getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('biosample')


from pydantic import Schema, create_model
import pydantic
from typing import Dict, List
import datetime

#m = list(es.client.indices.get_mapping(
#    'sra_experiment').values())[0]['mappings']['properties']

m = get_mapping_properties('sra_experiment')

def mappings(x):
    z = {}
    c = {}
    for k in x.keys():
        if ('type' in x[k]):
            if (x[k]['type'] == 'text'):
                z[k] = (str,
                        Schema(None,
                               title=k,
                               description=f'this is the {k} field'))
            if (x[k]['type'] == 'boolean'):
                z[k] = (bool,
                        Schema(None,
                               title=k,
                               description=f'this is the {k} field'))
            if (x[k]['type'] == 'date'):
                z[k] = (str,
                        Schema(None,
                               title=k,
                               description=f'this is the {k} field'))
            if (x[k]['type'] == 'long'):
                z[k] = (int,
                        Schema(None,
                               title=k,
                               description=f'this is the {k} field'))
            if (x[k]['type'] == 'float'):
                z[k] = (float,
                        Schema(None,
                               title=k,
                               description=f'this is the {k} field'))
            if (x[k]['type'] == 'nested'):
                c[k.title()] = create_model(k.title() + 'Record',
                                            **mappings(x[k]['properties']))
                z[k] = (List[c[k.title()]], [])
        # if('properties' in x[k]):
        #     locals()[k.title()] = create_model(k.title()+'Record', **mappings(x[k]['properties']))
        #     z[k] = (locals()[k.title()]],{})

    return (z)


@app.get("/experiment/{accession}",
         tags=['SRA'],
         response_model=create_model('Experiment1', **mappings(m)))
async def get_experiment_accession(
        getter: GetByAccession = Depends(GetByAccession)):
    return getter.get('sra_experiment')


class SimpleQueryStringSearch():
    """Basic lucene query string search
    """
    def __init__(
            self,
            q: str = Query(None,
                           description="The query, using lucene query syntax",
                           example="cancer AND published:[2018-01-01 TO *]"),
            size: int = Query(10, gte=0, lt=1000, example=10),
            cursor: str = None,
            facets: List[str] = Query(
                [],
                description=('A list of strings identifying fields '
                             'for faceted search results. Simple '
                             'term faceting is used here, meaning '
                             'that fields that are short text and repeated '
                             'across records will be binned and counted.'),
                example=['center_name'],
            )):
        self.q = q
        self.size = size
        self.facets = facets
        self.cursor = cursor

    def _create_search_after(self, hit):
        """Create a cursor
        
        currently, implemented as simply using the 'id' field. 
        """
        from .cursor import encode_cursor
        # TODO: implement sorting here
        return encode_cursor(sort_dict=[{"_id": "asc"}], resp=hit.meta.id)

    def _resolve_search_after(self, cursor_string):
        from .cursor import decode_cursor
        (sort_dict, id) = decode_cursor(cursor_string)
        return (sort_dict, id)

    def search(self, index):
        searcher = Search(index=index)
        from .luqum_helper import (get_query_builder, get_query_translation)
        s = searcher.update_from_dict({"track_total_hits": True})[0:self.size]
        if (self.q is not None):
            builder = get_query_builder(index)
            translation = get_query_translation(builder, self.q)
            s = searcher.update_from_dict({
                "track_total_hits": True,
                "query": translation
            })
        # s = search.index(index).query('query_string',
        #                               query=self.q)[0:self.size]
        for agg in self.facets:
            # these update the s object in place
            # as opposed to the query method(s) that
            # return a new copied object
            if agg.endswith('.keyword'):
                s.aggs.bucket(agg, 'terms', field=agg)
            else:
                s.aggs.bucket(agg, 'terms', field=agg+'.keyword')                
        s = s.sort({"_id": {"order": "asc"}})
        if (self.cursor is not None):
            s = s.extra(
                search_after=[self._resolve_search_after(self.cursor)[1]])
        resp = s[0:self.size].execute()
        hits = list([res for res in resp])
        # cursor
        search_after = None
        if (len(hits) == self.size and self.size > 0):
            search_after = self._create_search_after(hits[-1])

        return {
            "hits": [res.to_dict() for res in resp],
            "facets": resp.aggs.to_dict(),
            "cursor": search_after,
            "stats": {
                "total": resp.hits.total.value,
                "took": resp.took
            },
            "success": resp.success()
        }
    
@app.get("/studies/search", tags=['SRA'], response_model=ResponseModel)
async def search_studies(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_study')


@app.get("/experiments/search", tags=['SRA'], response_model=ResponseModel)
async def search_experiments(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_experiment')


@app.get("/runs/search", tags=['SRA'], response_model=ResponseModel)
async def search_runs(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_run')


@app.get("/samples/search", tags=['SRA'], response_model=ResponseModel)
async def search_samples(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('sra_sample')


@app.get("/biosample/search", tags=['Biosample'], response_model=ResponseModel)
async def search_biosamples(
        searcher: SimpleQueryStringSearch = Depends(SimpleQueryStringSearch)):
    return searcher.search('biosample')


# @app.get("/sql", tags=["SQL"])
# async def elasticsearch_sql(
#         query: str = Query(
#             ...,
#             example="SELECT * FROM sra_study WHERE QUERY('breast cancer')",
#             description=('And Elasticsearch SQL query. See the '
#                          'endpoint description for more details.'),
#         ),
#         cursor: str = Query(
#             None,
#             description=('The cursor returned by a large result '
#                          'set can be used here to fetch the next '
#                          'set of results.'),
#         ),
#         size: int = Query(
#             500,
#             gte=0,
#             lt=1000,
#             example=10,
#             description=('The size of the result set to return. '
#                          'Minimum: 0, maximum: 1000. Use the '
#                          '`cursor` functionality to loop over result '
#                          'sets larger than `size`.'),
#         )):
#     """Use Elasticsearch SQL to get results.

#     Elasticsearch SQL has some [limitations](https://www.elastic.co/guide/en/elasticsearch/reference/7.0/sql-limitations.html) relative to regular relational
#     databases. In particular, there are no
#     "joins" available in Elasticsearch SQL.

#     See:
#       - [elasticsearch SQL documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-syntax-select.html)
#       - [An Introduction to Elasticsearch SQL with Practical Examples - Part 1](https://www.elastic.co/blog/an-introduction-to-elasticsearch-sql-with-practical-examples-part-1)
#       - [An Introduction to Elasticsearch SQL with Practical Examples - Part 2](https://www.elastic.co/blog/an-introduction-to-elasticsearch-sql-with-practical-examples-part-2)
#       - [Elasticsearch functions and operators](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions.html)

#     ## Example queries

#     These example queries can be pasted into the `query` field on
#     the online docs or can be used in the `query` field from a
#     client. Note that it may be beneficial to change the default
#     `size` field to a larger value (up to the maximum). For `GROUP BY`
#     queries, there is an intrinsic limit of 512 records, so specifying
#     `LIMIT` greater than 512 will result in errors.

#     Select all top-level fields from sra studies. Note that the
#     result will include a `cursor` field. Supply the `cursor` string
#     to the cursor field and rerun the query to get the next batch
#     of results.

#     ```
#     select * from sra_study
#     ```

#     Get a count of the visibility (open, controlled access, etc.) from all studies.

#     ```
#     select visibility, count(*)
#     from sra_study
#     group by visibility
#     ```

#     Get a count of the number of studies publised by month.

#     ```
#     select MONTH(published) as month,
#            YEAR(published) as year,
#            count(*)
#     from sra_study
#     group by month, year
#     order by year desc, month desc
#     ```
#     Perform a full text search on experiments and get a count of records.

#     ```
#     select count(*) as experiment_count
#     from sra_experiment
#     where QUERY('cancer')
#     ```

#     And get a count of the library_strategies associated with those
#     experiments.

#     ```
#     select count(*) as experiment_count, library_strategy
#     from sra_experiment
#     where QUERY('cancer')
#     group by library_strategy
#     order by experiment_count desc
#     limit 100
#     ```

#     """
#     try:
#         if (cursor is not None):
#             return es.client.transport.perform_request('POST',
#                                                        '/_xpack/sql',
#                                                        body={"cursor": cursor})
#         return es.client.transport.perform_request('POST',
#                                                    '/_xpack/sql',
#                                                    body={
#                                                        "query": query,
#                                                        "fetch_size": size
#                                                    })

#     except elasticsearch.exceptions.TransportError as e:
#         return e.info['error'], 400

# class ExtendedSearch(BaseModel):
#     """This encapsulates all the pieces of an
#     extendedQuery. The only required field is
#     the `query` field. See [the Elasticsearch query
#     DSL documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
#     for how to construct a query.
#     """
#     query: dict = Schema(..., example={"query_string": {"query": "cancer"}})
#     aggs: dict = Schema({}, description="Aggregates")
#     size: int = Schema(10,
#                        description=('The maximum number of records to return'),
#                        gte=0,
#                        lte=1000,
#                        example=10)
#     filter: dict = Schema({}, description="Filters")
#     search_after: List[Any] = Schema([],
#                                      description="search_after functionality",
#                                      example=[])
#     sort: List[dict] = Schema(
#         [{
#             "_score": "desc"
#         }],
#         description="sort by",
#         example=[{
#             "_id": "asc"
#         }],
#     )

#     def do_search(self, index):
#         """do a full elasticsearch search

#         index: str
#             the elasticsearch index

#         returns the raw elasticsearch response.
#         """
#         body_dict = self.dict()

#         # need to clean up defaults
#         if (len(body_dict['aggs']) == 0):
#             del (body_dict['aggs'])

#         if (len(body_dict['search_after']) == 0):
#             del (body_dict['search_after'])
#         elif (len(body_dict['search_after']) == 1):
#             if (body_dict['search_after'][0] is None):
#                 del (body_dict['search_after'])

#         if (len(body_dict['sort']) == 1):
#             if (body_dict['sort'][0] == {}):
#                 body_dict['sort'] = [{'_id': 'asc'}]

#         if (len(body_dict['filter']) == 0):
#             del (body_dict['filter'])

#         resp = es.client.search(index=index, body=body_dict)

#         # returns raw elasticsearch response
#         return resp

# @app.post("/studies/extendedSearch", tags=["SRA", "Search"])
# def extended_study_search(body: ExtendedSearch):
#     return body.do_search('sra_study')

# @app.post("/samples/extendedSearch", tags=["SRA", "Search"])
# def extended_samples_search(body: ExtendedSearch):
#     return body.do_search('sra_sample')

# @app.post("/experiments/extendedSearch", tags=["SRA", "Search"])
# def extended_experiment_search(body: ExtendedSearch):
#     return body.do_search('sra_experiment')

# @app.post("/runs/extendedSearch", tags=["SRA", "Search"])
# def extended_study_search(body: ExtendedSearch):
#     return body.do_search('sra_run')


def abc(mappings):
    print(mappings)
    fields = []
    for k, v in mappings.items():
        keyword = False
        if ('fields' in v):
            if ('keyword' in v['fields']):
                keyword = True
        fields.append((k, v['type'], keyword))
    return fields


@app.get("/_mapping/{entity}")
def mapping(entity: str) -> dict:
    return get_flattened_mapping_from_index('sra_'+entity)
