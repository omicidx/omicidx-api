"""Just convenience functions for elasticsearch"""
from .elastic_connection import connections
from elasticsearch_dsl import Index
from typing import List
from .field_descriptors import fulltext_fields

def get_mapping_properties(index: str) -> dict:
    """Get the "properties" mappings from an elasticsearch index
    
    Parameters
    ----------
    index: str 
        The name of the index to get mappings from
    
    Returns
    -------
    dict starting with the properties of the mapping
    """
    mapping_properties = list(Index(index)
                              .get_mapping()
                              .values())[0]['mappings']['properties']
    return mapping_properties


def flatten_mapping(mapping, parent=None, nested=False):
    """flatten full mapping down to dotted names"""
    ret = []
    for k, v in mapping.items():
        # created dotted fields recursively
        if(parent is not None):
            k = parent + '.' + k
        # set up ret object
        obj= {}
        obj['field']=k

        # nested will be true for truly nested fields
        # TODO: may need to add path for the nesting to
        # simplify downstream use
        obj['nested'] = nested
        if(nested):
            obj['path'] = parent

        # this is either nested or regular field
        if('type' in v):
            # deal with nested fields
            if(v['type']=='nested'):
                obj['type']='object'
                # recursively follow nested objects
                ret+=flatten_mapping(v['properties'], parent=k, nested=True)
            # deal with "regular fields"
            else:
                obj['type']=v['type']
                # look for fields (such as keyword, etc.)
                if('fields' in v):
                    # if keyword, add as a boolean flag
                    # to mark for term searches and aggs
                    if('keyword' in v['fields']):
                        obj['keyword']=True
                ret+=[obj]
        # Just an embedded object
        else:
            obj['type']='object'
            # recursively follow embedded objects
            ret+=flatten_mapping(v['properties'], parent=k)
    return(ret)


def get_flattened_mapping_from_index(index):
    return flatten_mapping(get_mapping_properties(index))

def available_facets_by_index(index):
    """Return the available facet fields for an index"""

    available_fields = get_flattened_mapping_from_index(index)

    def should_be_facet_field(field: dict):
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

        # right now, only keyword fields (of type text) qualify
        if not (field['type'] == 'text' and field['keyword']):
            return False
        # filter out known full text fields
        # TODO: these should be changed in the elasticsearch mappings
        for ftf in fulltext_fields:
            if (field['field'].endswith(ftf)):
                return False
        return True

    facet_fields = filter(should_be_facet_field, available_fields)
    facet_names = list([f['field'] for f in facet_fields])
    return facet_names
