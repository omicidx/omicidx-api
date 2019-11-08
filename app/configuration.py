"""Configuration

"OMICIDX_CONFIGURATION_FILE" contains the path to a configuration file in toml format.

Example

```
[google]
project = "isb-cgc-01-0006"

[google.bigquery]
dataset = "omicidx"
etl_dataset = "omicidx_etl"

[elasticsearch]
nodes = "https://USER:PASSWORD@45e419eb0aef4f3d92cc7b6e5d1dc345.us-east-1.aws.found.io:9243"

[google.storage]
staging = "gs://temp-testing/abc/"
export = "gs://omicidx-cancerdatasci-org/exports/"
```

"""

import toml
import os

def get_configfile_location():
    """Get toml config file location

    Assumes that an environment variable, "OMICIDX_CONFIGURATION_FILE"
    contains the path to a configuration file in toml format

    Returns:
    str
    """
    return os.environ.get('OMICIDX_CONFIGURATION_FILE', 'config.toml')

class Config(dict):
    def __init__(self, configfile: str = None):

        configfile_location = configfile
        if(configfile is None):
            configfile_location = get_configfile_location()

        self.update(toml.load(configfile_location))

config = Config()
