
#######
# Do  #
# not #
# Use #
#######

"""Create classes that look like:

m = Mapping.from_es('sra_sample', using='default')

class Sample(dsl.Document):

    class Meta:
        mapping = m

    class Index:
        name = 'sra_sample'


class ESample(ElasticsearchObjectType):
    class Meta:
        document = Sample
        interfaces = (NewNode,)
        filter_backends = [
            FilteringFilterBackend,
            SearchFilterBackend,
            HighlightFilterBackend,
            OrderingFilterBackend,
            FacetedSearchFilterBackend,
            #DefaultOrderingFilterBackend,
        ]
        filter_fields = {
            'status': {'field': 'status.keyword'},
            'accession': 'accession.keyword', 
            'center_name': {"field": 'center_name.keyword'},
            'taxon_ids': {'field': 'taxon_ids',
                         'lookups': [
                             LOOKUP_FILTER_TERM,
                             LOOKUP_FILTER_TERMS,
                             LOOKUP_QUERY_IN,
                             LOOKUP_QUERY_EXCLUDE,
                         ],
                         }
        }
        search_fields = {
            'title': None,
            'abstract': None,
            'center_name': None,
            'description': None
        }
        ordering_fields = {
            'accession': 'accession.keyword', 
            'received': None,
            'published': None,
            'lastupdate': None
        }

        faceted_search_fields = {
            'taxon_id': {
                'field': 'taxon_id',
                # 'enabled': True,  # Will appear in the list by default
                # 'global': True, # Will ignore query when doing aggregation
            },
            'study_type': {
                'field': 'study.study_type'
            },
            'published': {
                'field': 'published',
                'facet': DateHistogramFacet,
                'options': {
                    'interval': 'month',
                }
            }
        }
        highlight_fields = {
            'title': {
                'enabled': True,
                'options': {
                    'pre_tags': ["<b>"],
                    'post_tags': ["</b>"],
                }
            },
            'abstract': {
                'options': {
                    'fragment_size': 50,
                    'number_of_fragments': 3
                }
            },
            'category': {},
        }


SampleDocument = ge.ElasticsearchConnectionField(ESample)

Then use as:

class Query(graphene.ObjectType):
    SampleQuery = SampleDocument

schema = graphene.Schema(query = Query)

"""


import elasticsearch_dsl
from graphene.relay.node import Node
from graphene_elastic import ElasticsearchObjectType


def create_document_type(document_name: str,
                         mapping: elasticsearch_dsl.Mapping,
                         index: str) -> elasticsearch_dsl.Document:
    """Create an elasticsearch_dsl.Document from mapping and index name

    Parameters
    ----------
    document_name: str
        The name of the document type
    mapping: elasticsearch_dsl.Mapping
        Often obtained by Mapping.from_es('INDEX_NAME', 'default')

    Returns
    -------
    class of type elasticsearch_dsl.Document named document_name
    """
    
    # make Meta inner class
    meta_class = type(document_name+"Meta", (object,), {'mapping': mapping})

    # make Index inner
    index_class = type(document_name+"Index", (object,), {'name': index})

    # and return class with document_name
    return type(document_name, (elasticsearch_dsl.Document, ), { # replace object with elasticsearch_dsl.Document
        'Meta': meta_class,
        'Index': index_class
    })

def create_connection_type(document_type: elasticsearch_dsl.Document,
                           interfaces: tuple = (Node,),
                           doc_name_prefix: str = 'EOT',
                           **kwargs):
    kwargs.update({
        'document': document_type,
        'interfaces': interfaces})
    
    meta_class = type(document_type.__name__+"Meta", (object,), kwargs)

    return type(doc_name_prefix+document_type.__name__,
                (ElasticsearchObjectType,),
                {'Meta': meta_class})
