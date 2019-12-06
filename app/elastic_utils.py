"""Just convenience functions for elasticsearch"""
from .elastic_connection import connections
from elasticsearch_dsl import Index

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
