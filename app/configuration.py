"""Configuration

Environment variables:



```
self.BIGQUERY_PRODUCTION_DATASET = os.getenv('BIGQUERY_PRODUCTION_DATASET')
self.BIGQUERY_ETL_DATASET = os.getenv('BIGQUERY_ETL_DATASET')
self.ELASTICSEARCH_NODES = os.getenv('ELASTICSEARCH_NODES')
self.GCS_STAGING_BUCKET =  os.getenv['GCS_STAGING_BUCKET'] 
self.GCS_PUBLIC_BUCKET =  os.getenv['GCS_PUBLIC_BUCKET']
```

Example ELASTICSEARCH_NODES:

"https://USER:PASSWORD@45e419eb0aef4f3d92cc7b6e5d1dc345.us-east-1.aws.found.io:9243"

Example GCS_PUBLIC_BUCKET

"gs://temp-testing/abc/"
"""
import os

class Config(object):
    def __init__(self):
        self.ELASTICSEARCH_NODES = os.getenv('ELASTICSEARCH_NODES')
        # Everything below here unused!!!
        # TODO: decide if these are worth keeping....
        self.BIGQUERY_ETL_DATASET = os.getenv('BIGQUERY_ETL_DATASET')
        self.BIGQUERY_PRODUCTION_DATASET = os.getenv('BIGQUERY_PRODUCTION_DATASET')
        self.GCS_STAGING_BUCKET =  os.getenv('GCS_STAGING_BUCKET')
        self.GCS_PUBLIC_BUCKET =  os.getenv('GCS_PUBLIC_BUCKET')

config = Config()
