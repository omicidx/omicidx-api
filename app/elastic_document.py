# GraphQL 
import elasticsearch_dsl
import graphene
from elasticsearch_dsl import (Document, Index, Mapping)


def create_document_from_es_index(name: str, index: str, using: str = 'default'):
    """Create an elasticsearch_dsl Document

    Before using this function, it is necessary to create a connection
    on the elasticsearch_dsl global connections object. Afterwards,
    calling this function will create and return an elasticsearch_dsl.Document
    populated with a mapping from the pre-existing index in elasticsearch.

    Parameters
    ----------
    name: str
        The string name for the resulting class
    index: str
        The string name for the elasticsearch index
    using: str
        The connection name to use (assumes that this exists or was 
        already created. Defaults to 'default'.

    Return
    ------
    An `elasticsearch_dsl.Document` with type `name` based on existing
    elasticsearch index, `index`.
    """
    class LocalMeta:
        mapping = elasticsearch_dsl.Mapping.from_es(index, using = using)
    class LocalIndex:
        name = index
    document = type(name, (Document,), {"Meta": LocalMeta,
                                        "Index": LocalIndex})

    return document

def base_object_type_from_document(document: Document) -> graphene.ObjectType:
    pass

def add_aggregates_to_existing_object_type(obj: graphene.ObjectType) -> graphene.ObjectType:
    pass

def create_input_object_type_from_document(document: Document) -> graphene.InputObjectType:
    pass

def create_resolver_for_object(obj: graphene.ObjectType, inputobj: graphene.InputObjectType):
    pass
