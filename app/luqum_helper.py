"""Luqum helpers

The luqum package 

"""
import luqum
from elasticsearch_dsl import (Index, connections)
from luqum.elasticsearch import (SchemaAnalyzer, ElasticsearchQueryBuilder)
from luqum.parser import (parser, ParseError)
from luqum.tree import (SearchField, OrOperation, Word, Group)

try:
    import ujson as json
except:
    import json as json


class BareTextTransformer(luqum.utils.LuceneTreeTransformer):
    """Convert bare Words or Phrases to full text search

    In cases where a query string has bare text (no field
    association), we want to construct a DSL query that includes
    all fields in an OR configuration to perform the full
    text search against all fields. 
    This class can walk the tree and convert bare Word 
    nodes into the required set of SearchField objects. Note 
    that this is entirely equivalent to `multi_match` in terms
    of performance, etc. 
    """
    def __init__(self, fields=['title', 'abstract']):
        """Create a new BareTextTransformer
        Parameters
        ----------
        fields: list of str
            This is the list of fields that will used to 
            create the composite SearchField objects that
            will be OR'ed together to simulate full text
            search.
        
        Returns
        -------
        None. The tree is modified in place.
        """
        super()
        self.fields = fields

    def visit_word(self, node, parent):
        if (len(parent) > 0 and (isinstance(parent[-1], luqum.tree.SearchField)
                                 or isinstance(parent[-1], luqum.tree.Range))):
            return node
        else:
            search_list = [SearchField(f, node) for f in self.fields]
            return Group(OrOperation(*search_list))

    def visit_phrase(self, node, parent):
        if (len(parent) > 0 and (isinstance(parent[-1], luqum.tree.SearchField)
                                 or isinstance(parent[-1], luqum.tree.Range))):
            return node
        else:
            search_list = [SearchField(f, node) for f in self.fields]
            return Group(OrOperation(*search_list))


def get_query_builder(index: str) -> ElasticsearchQueryBuilder:
    """
    """
    properties = list(Index(index).get_mapping().values())[0]['mappings']
    # this is just what luqum wants....
    schema_analyzer = SchemaAnalyzer({"mappings": {"doc": properties}})
    es_builder = ElasticsearchQueryBuilder(
        **schema_analyzer.query_builder_options())
    return es_builder
    # tree = parser.parse(q)
    # query = es_builder(tree)


def get_query_translation(builder, q, **kwargs):
    try:
        tree = parser.parse(q)
        transformer = BareTextTransformer()
        tree = transformer.visit(tree)
        return builder(tree)
    except ParseError as e:
        # TODO better error message (text)
        # TODO return error in response
        print(e)
