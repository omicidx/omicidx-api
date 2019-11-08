import configparser
import certifi
from elasticsearch import Elasticsearch
from .configuration import config

class ESClient(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.client = self._get_client()
    
    def _get_client(self) -> Elasticsearch:
        """Get an elasticsearch client

        :param: configfile 
        :type: string"""
        es_config = config['elasticsearch']
        es = Elasticsearch(
            hosts = es_config['nodes'],
            **self.kwargs
        )
        return(es)

def main():
    """Allow command-line access to elasticsearch_dsl

    poetry run python -m app.esclient

    """
    
    from IPython import embed
    from elasticsearch_dsl import connections, Search, Index, Mapping

    es = ESClient()

    connections.add_connection('default', es.client)

    embed()

    
if __name__ == '__main__':
    main()
