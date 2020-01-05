from fastapi import (Path, Query, HTTPException)
from typing import (List)
from .elastic_connection import connections
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search
from .elastic_utils import available_facets_by_index


class GetByAccession():
    def __init__(self,
                 accession: str = Path(...,
                                       description="An accession for lookup"),
                 
                 include_fields: List[str] = Query([], description = ("Fields to include in results. The default is to "
                                                                      "all fields (*)"),
                                                   example = ['*']),
                 
                 exclude_fields: List[str] =  Query([], description = ("Fields to exclude from results. The default is to "
                                                                       "not exclude any fields. ")),

    ):
        self.accession = accession
        self.include_fields = include_fields
        self.exclude_fields = exclude_fields
        if(len(include_fields)==0):
            self.include_fields = ['*']


    def get(self, index, doc_type="_doc"):
        try:
            return connections.get_connection().get(
                index=index,
                doc_type=doc_type,
                id=self.accession,
                _source_includes = self.include_fields,
                _source_excludes = self.exclude_fields
            )['_source']
        except NotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail=f"Accession {self.accession} not found in index {index}."
            )


class GetSubResource():
    def __init__(self,
                 accession: str = Path(...,
                                       description="An accession for lookup"),
                 include_fields: List[str] = Query([], description = ("Fields to include in results. The default is to "
                                                                      "all fields (*)"),
                                                   example = ['*']),
                 
                 exclude_fields: List[str] =  Query([], description = ("Fields to exclude from results. The default is to "
                                                                       "not exclude any fields. ")),
                 
                 size: int = Query(10, gte=0, lt=1000, example=10),
                 cursor: str = None):
        self.accession = accession
        self.size = size
        self.cursor = cursor
        self.include_fields = include_fields
        self.exclude_fields = exclude_fields
        if(len(include_fields)==0):
            self.include_fields = ['*']


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

    def get(self, resource, subresource, doc_type='_doc'):
        try:
            connections.get_connection().get(index=resource,
                                             doc_type=doc_type,
                                             id=self.accession)['_source']
        except NotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail=
                f"Accession {self.accession} not found in index {resource}.")
        resource_name = resource.replace('sra_', '')
        s = (Search().index(subresource).update_from_dict({
            "query": {
                'term': {
                    resource_name + ".accession.keyword": self.accession
                }
            }
        }))
        s = s.update_from_dict({"track_total_hits": True})
        s = s.sort({"_id": {"order": "asc"}})
        if (self.cursor is not None):
            s = s.extra(
                search_after=[self._resolve_search_after(self.cursor)[1]])
        s = s.extra(_source = {"include": self.include_fields, "exclude": self.exclude_fields})
        resp = s[0:self.size].execute()
        hits = list([res for res in resp])
        # cursor
        search_after = None
        if (len(hits) == self.size and self.size > 0):
            search_after = self._create_search_after(hits[-1])

        return {
            "hits": [res.to_dict() for res in resp],
            "cursor": search_after,
            "stats": {
                "total": resp.hits.total.value,
                "took": resp.took
            },
            "success": resp.success()
        }


class SimpleQueryStringSearch():
    """Basic lucene query string search
    """
    def __init__(
            self,
            q: str = Query(None,
                           description="The query, using [lucene query syntax](https://lucene.apache.org/core/3_6_0/queryparsersyntax.html]",
                           example="cancer"),
            
            size: int = Query(10, gte=0, lt=1000, example=10),

            cursor: str = Query(None, description = ("The cursor is used to scroll through results. For a query "
                                                     "with more results than `size`, the result will include `cursor` "
                                                     "in the result json. Use that value here and re-issue the query. "
                                                     "The next set or results will be returned. When no more results are "
                                                     "available, the `cursor` will again be empty in the result json.")),
            
            facet_size: int = Query(10, gte=1, lte=1000, example=10,
                                    description = (
                                        "The maximum number of records returned for each facet. "
                                        "This has no effect unless one or more facets are specified."
                                    )
            ),
            
            include_fields: List[str] = Query([], description = ("Fields to include in results. The default is to "
                                                      "all fields (*)"),
                                   example = ['*']),

            exclude_fields: List[str] =  Query([], description = ("Fields to exclude from results. The default is to "
                                                      "not exclude any fields. ")),
            
            facets: List[str] = Query(
                [],
                description=('A list of strings identifying fields '
                             'for faceted search results. Simple '
                             'term faceting is used here, meaning '
                             'that fields that are short text and repeated '
                             'across records will be binned and counted.'),
                #example=['center_name'],
            )):
        self.q = q
        self.size = size
        self.include_fields = include_fields
        self.exclude_fields = exclude_fields
        if(len(include_fields)==0):
            self.include_fields = ['*']
        self.facets = facets
        self.cursor = cursor
        self.facet_size = facet_size

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

    def _transform_facet_results_to_list(self, facet_results):
        d = []
        for fieldname in facet_results.keys():
            buckets = facet_results[fieldname]['buckets'].copy()
            facet_results[fieldname].pop( 'buckets')
            d.append({"field": fieldname,
                      "results": buckets,
                      "meta": facet_results[fieldname]})
        return d

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
        available_facets = available_facets_by_index(index)
        for agg in self.facets:
            # these update the s object in place
            # as opposed to the query method(s) that
            # return a new copied object
            if not agg in available_facets:
                logging.info(f'skipping agg {agg}')
                continue
            if not agg.endswith('.keyword'):
                agg = agg + '.keyword'
            s.aggs.bucket(agg.replace('.keyword', ''), 'terms', field=agg,
                          size=self.facet_size)

        s = s.sort({"_id": {"order": "asc"}})
        if (self.cursor is not None):
            s = s.extra(
                search_after=[self._resolve_search_after(self.cursor)[1]])
        s = s.extra(_source = {"include": self.include_fields, "exclude": self.exclude_fields})
        resp = s[0:self.size].execute()
        hits = list([res for res in resp])
        # cursor
        search_after = None
        if (len(hits) == self.size and self.size > 0):
            search_after = self._create_search_after(hits[-1])

        return {
            "hits": [res.to_dict() for res in resp],
            "facets": self._transform_facet_results_to_list( resp.aggs.to_dict()),
            "cursor": search_after,
            "stats": {
                "total": resp.hits.total.value,
                "took": resp.took
            },
            "success": resp.success()
        }
