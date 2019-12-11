from fastapi import (Path, Query, HTTPException)
from typing import (List)
from .elastic_connection import connections
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search
from .elastic_utils import available_facets_by_index


class GetByAccession():
    def __init__(self,
                 accession: str = Path(...,
                                       description="An accession for lookup")):
        self.accession = accession

    def get(self, index, doc_type="_doc"):
        try:
            return connections.get_connection().get(
                index=index, doc_type=doc_type, id=self.accession)['_source']
        except NotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail=f"Accession {self.accession} not found in index {index}."
            )


class GetSubResource():
    def __init__(self,
                 accession: str = Path(...,
                                       description="An accession for lookup"),
                 size: int = Query(10, gte=0, lt=1000, example=10),
                 cursor: str = None):
        self.accession = accession
        self.size = size
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
        s = s.sort({"_id": {"order": "asc"}})
        if (self.cursor is not None):
            s = s.extra(
                search_after=[self._resolve_search_after(self.cursor)[1]])
        print(s.to_dict())
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
                           description="The query, using lucene query syntax",
                           example="cancer AND osteosarcoma"),
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
        available_facets = available_facets_by_index(index)
        print(available_facets)
        for agg in self.facets:
            # these update the s object in place
            # as opposed to the query method(s) that
            # return a new copied object
            if not agg in available_facets:
                logging.info(f'skipping agg {agg}')
                continue
            if not agg.endswith('.keyword'):
                agg = agg + '.keyword'
            s.aggs.bucket(agg.replace('.keyword', ''), 'terms', field=agg)

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
