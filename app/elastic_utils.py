"""Just convenience functions for elasticsearch"""
from .elastic_connection import connections
from elasticsearch_dsl import Index
from typing import Tuple
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
    ret = {}
    for k, v in mapping.items():
        # created dotted fields recursively
        if(parent is not None):
            k = parent + '.' + k
        # set up ret object
        ret[k] = {}

        # nested will be true for truly nested fields
        # TODO: may need to add path for the nesting to
        # simplify downstream use
        ret[k]['nested'] = nested
        if(nested):
            ret[k]['path'] = parent

        # this is either nested or regular field
        if('type' in v):
            # deal with nested fields
            if(v['type']=='nested'):
                ret[k]['type']='object'
                # recursively follow nested objects
                ret.update(flatten_mapping(v['properties'], parent=k, nested=True))
            # deal with "regular fields"
            else:
                ret[k]['type']=v['type']
                # look for fields (such as keyword, etc.)
                if('fields' in v):
                    # if keyword, add as a boolean flag
                    # to mark for term searches and aggs
                    if('keyword' in v['fields']):
                        ret[k]['keyword']=True
        # Just an embedded object
        else:
            ret[k]['type']='object'
            # recursively follow embedded objects
            ret.update(flatten_mapping(v['properties'], parent=k))
    return(ret)


def get_flattened_mapping_from_index(index):
    return flatten_mapping(get_mapping_properties(index))

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
