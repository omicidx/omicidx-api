from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from fastapi import (FastAPI, HTTPException, Query, Depends, Path)
from pydantic import (BaseModel, ValidationError, validator, Schema)
from starlette.responses import RedirectResponse
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.graphql import GraphQLApp
from typing import (Dict, List, Any, Tuple)
from elasticsearch_dsl import Search, Index
import elasticsearch

from .response_models import (ResponseModel, MappingResults)
from .field_descriptors import fulltext_fields
from .elastic_connection import connections
from .elastic_utils import (get_mapping_properties,
                            get_flattened_mapping_from_index,
)
from .routers import (sra, biosample)

import logging


#from .schema import schema

# REST API models
import omicidx.sra.pydantic_models as p
from .dependers import (GetByAccession, GetSubResource, SimpleQueryStringSearch)
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
app.include_router(sra.router, prefix='/sra')
app.include_router(biosample.router, prefix='/biosample')

#from .schema.schema import schema
#app.add_route('/graphql', GraphQLApp(schema=schema))


# for now, redirect to the docs directly
@app.route("/")
async def home(request: Request):
    return RedirectResponse(url='/docs')





from pydantic import Schema, create_model
import pydantic
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


# moved to routers
# @app.get("/experiment/{accession}",
#          tags=['SRA'],
#          response_model=create_model('Experiment1', **mappings(m)))
# async def get_experiment_accession(
#         getter: GetByAccession = Depends(GetByAccession)):
#     return getter.get('sra_experiment')


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
    if(entity!="biosample"):
        return get_flattened_mapping_from_index('sra_' + entity)
    return get_flattened_mapping_from_index(biosample)

# TODO: this is now duplicated in elastic_utils--need to refactor
@app.get("/facets/{index}", response_model=List[str])
def available_facets_by_index(index):
    """Return the available facet fields for an index"""

    available_fields = get_flattened_mapping_from_index(index)

    def should_be_facet_field(field: Tuple[str, dict]):
        """Use as filter for fields to find available facet fields

        Parameters
        ----------
        field: Tuple[str, dict]
            first field is name of field and the dict describes the
            type, etc.
        
        Returns
        -------
        bool
            True if to include field as aggregatable, False otherwise
        """
        k, v = field  # unpack tuple

        # right now, only keyword fields (of type text) qualify
        if not (v['type'] == 'text' and v['keyword']):
            return False
        # filter out known full text fields
        # TODO: these should be changed in the elasticsearch mappings
        for ftf in fulltext_fields:
            if (k.endswith(ftf)):
                return False
        return True

    facets = dict(filter(should_be_facet_field, available_fields.items()))
    facet_names = list(facets.keys())
    return facet_names
