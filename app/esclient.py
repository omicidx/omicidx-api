import configparser
import certifi
from elasticsearch import Elasticsearch

class ESClient():
    def __init__(self, configfile):
        self.client = self._get_client(configfile)
    
    def _get_client(self, configfile):
        """Get an elasticsearch client

        :param: configfile 
        :type: string"""
        config = configparser.ConfigParser()
        config.read(configfile)
        es_config = config['elasticsearch']
        es = Elasticsearch(
            hosts = es_config['nodes'],
            http_auth=(es_config['user'], es_config['password'])
        )
        return(es)
