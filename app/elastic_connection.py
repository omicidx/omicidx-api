"""Set up elasticsearch_dsl connections

Uses central configuration.py to get config information.

Creates a 'default' alias on elasticsearch_dsl connections
global. To use:

>>> from elastic_connection import connections
>>> Search().index('sra_study').count()
>>> Index('sra_study').get_mapping()
>>> con = connections.get_connection()

Equivalent to:

>>> con = connections.get_connection('default')

The `con` is now a basic elasticsearch client.

"""
import elasticsearch_dsl
import os
import certifi
import elasticsearch_dsl.connections as connections

from elasticsearch import Elasticsearch
from typing import List

from .configuration import config

def init_connection_object():
    connections.create_connection(
        alias='default',
        hosts=config.ELASTICSEARCH_NODES
    )

init_connection_object()

    
def main():
    """Allow command-line access to elasticsearch_dsl

    poetry run python -m app.esclient

    then, you can do:

    >>> Search().index('sra_study').count()
    226823
    >>> Index('sra_study').get_mapping()
    ....
    >>> con = connections.get_connection()
    >>> con
    <Elasticsearch([{'host': '45e419eb0aef4f3d92cc7bdc345.us-east-1.aws.found.io', 'port': 9243, 'use_ssl': True, 'http_auth': 'USERNAME:PASSWORD'}])>
    """
    
    from IPython import embed
    from elasticsearch_dsl import Search, Index, Mapping

    print(x)
    embed()

if __name__ == '__main__':
    main()
    
