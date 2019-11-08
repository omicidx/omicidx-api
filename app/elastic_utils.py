import elasticsearch_dsl
import os
from typing import List
import elasticsearch_dsl.connections as connections


                            #######################
                            # ELASTICSEARCH STUFF #
                            #######################

def get_connection(alias: str = 'default'):
    """get a named elasticsearch_dsl connection

    Parameters
    ----------
    alias: str
        The alias/name for the connection. Should have been
        created earlier using `create_connection`. 

    Returns
    -------
    An elasticsearch connection
    """
    return connections.get_connection(alias = alias)


def create_connection(alias: str = 'default',
                      hosts: List[str] = [os.getenv('ES_HOST','http://localhost:9200')], **kwargs):
    """create an elasticsearch_dsl connection alias

    Parameters
    ----------
    alias: str
        The name for the connection. 
    **kwargs: args

    Return
    ------
    Nothing. Used for its side effects of creating a connection on the global connection object

    >>> create_connection(alias = 'default', hosts = ['https://user:pass@host:9243/'])
    """
    connections.create_connection(alias = alias, hosts = hosts, **kwargs)




def main():
    """Allow command-line access to elasticsearch_dsl

    poetry run python -m app.esclient

    Assumes that environment variable ES_HOST is set to something like:
    `https://user:pass@host:9243/`

    """
    
    from IPython import embed
    from elasticsearch_dsl import Search, Index, Mapping


    x = create_connection(alias = 'default',
                      hosts = [os.getenv('ES_HOST', 'http://localhost:9200')])
    print(x)
    embed()

if __name__ == '__main__':
    main()
    
