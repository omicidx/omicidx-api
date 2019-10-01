mappings = {
      "properties": {
        "status": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "lastupdate": {
          "type": "date",
          "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'||yyyy-MM-dd HH:mm:ss.SSSS 'UTC'||yyyy-MM-dd HH:mm:ss.SS 'UTC'||yyyy-MM-dd HH:mm:ss.S 'UTC'"
        },
        "xrefs": {
          "include_in_parent": True,
          "type": "nested",
          "properties": {
            "db": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "id": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            }
          }
        },
        "received": {
          "type": "date",
          "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'"
        },
        "description": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "insdc": {
          "type": "boolean"
        },
        "experiment_count": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "title": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "study": {
          "properties": {
            "broker_name": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "lastupdate": {
              "type": "date",
              "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'||yyyy-MM-dd HH:mm:ss.SSSS 'UTC'||yyyy-MM-dd HH:mm:ss.SS 'UTC'||yyyy-MM-dd HH:mm:ss.S 'UTC'"
            },
            "pubmed_ids": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "description": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "insdc": {
              "type": "boolean"
            },
            "received": {
              "type": "date",
              "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'"
            },
            "center_name": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "title": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "abstract": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "identifiers": {
              "include_in_parent": True,
              "type": "nested",
              "properties": {
                "namespace": {
                  "fields": {
                    "keyword": {
                      "ignore_above": 256,
                      "type": "keyword"
                    }
                  },
                  "type": "text"
                },
                "id": {
                  "fields": {
                    "keyword": {
                      "ignore_above": 256,
                      "type": "keyword"
                    }
                  },
                  "type": "text"
                }
              }
            },
            "accession": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "study_type": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "alias": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "status": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "BioProject": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "attributes": {
              "include_in_parent": True,
              "type": "nested",
              "properties": {
                "tag": {
                  "fields": {
                    "keyword": {
                      "ignore_above": 256,
                      "type": "keyword"
                    }
                  },
                  "type": "text"
                },
                "value": {
                  "fields": {
                    "keyword": {
                      "ignore_above": 256,
                      "type": "keyword"
                    }
                  },
                  "type": "text"
                }
              }
            },
            "published": {
              "type": "date",
              "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'"
            }
          }
        },
        "identifiers": {
          "include_in_parent": True,
          "type": "nested",
          "properties": {
            "namespace": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "id": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            }
          }
        },
        "mean_bases_per_run": {
          "type": "float"
        },
        "accession": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "total_spots": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "alias": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "BioSample": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "run_count": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "published": {
          "type": "date",
          "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'"
        },
        "taxon_id": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "attributes": {
          "properties": {
            "tag": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            },
            "value": {
              "type": "keyword"
            }
          }
        },
        "organism": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        },
        "total_bases": {
          "fields": {
            "keyword": {
              "ignore_above": 256,
              "type": "keyword"
            }
          },
          "type": "text"
        }
      },
      "dynamic_templates": [
        {
          "runs": {
            "mapping": {
              "type": "nested",
              "include_in_parent": True
            },
            "match": "runs"
          }
        },
        {
          "identifiers": {
            "mapping": {
              "type": "nested",
              "include_in_parent": True
            },
            "match": "identifiers"
          }
        },
        {
          "attributes": {
            "mapping": {
              "type": "nested",
              "include_in_parent": True
            },
            "match": "attributes"
          }
        },
        {
          "attribute_values": {
            "path_match": "*.attributes.value",
            "mapping": {
              "fields": {
                "keyword": {
                  "ignore_above": 256,
                  "type": "keyword"
                }
              },
              "type": "text"
            }
          }
        },
        {
          "published": {
            "mapping": {
              "type": "date",
              "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'"
            },
            "match": "published"
          }
        },
        {
          "received": {
            "mapping": {
              "type": "date",
              "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'"
            },
            "match": "received"
          }
        },
        {
          "generic_dates": {
            "mapping": {
              "type": "date",
              "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss+00:00||yyyy-MM-dd HH:mm:ss 'UTC'||yyyy-MM-dd HH:mm:ss.SSSS 'UTC'||yyyy-MM-dd HH:mm:ss.SS 'UTC'||yyyy-MM-dd HH:mm:ss.S 'UTC'"
            },
            "match": "*date"
          }
        },
        {
          "xrefs": {
            "mapping": {
              "type": "nested",
              "include_in_parent": True
            },
            "match": "xrefs"
          }
        },
        {
          "file_addons": {
            "mapping": {
              "type": "nested",
              "include_in_parent": True
            },
            "match": "file_addons"
          }
        },
        {
          "reads": {
            "mapping": {
              "type": "nested",
              "include_in_parent": True
            },
            "match": "reads"
          }
        },
        {
          "base_counts": {
            "mapping": {
              "type": "nested",
              "include_in_parent": True
            },
            "match": "base_counts"
          }
        },
        {
          "qualities": {
            "mapping": {
              "type": "nested",
              "include_in_parent": True
            },
            "match": "qualities"
          }
        }
      ]
    }

import graphene

def create_text_filters(field_name, keyword=True):
    d = {}
    def concat(string, field_name=field_name, sep="_"):
        if(string == ''):
            return field_name
        return field_name + sep + string
    d[concat('')] = graphene.String(description = 'equals')
    d[concat('not')] = graphene.String(description = "does not equal")
    d[concat('contains')] = graphene.String(description = "contains")
    d[concat('not_contains')] = graphene.String(description = "does not contain")
    return(d)

def return_io():
    g = {}
    for k, v in mappings['properties'].items():
        if('type' in v):
            if(v['type']=='text'):
                g.update(create_text_filters(k))
    return g



FilterInputType = type("FilterInputType", (graphene.InputObjectType,), return_io())
class newFilt(FilterInputType):
    or_ = graphene.Field(graphene.List(lambda: newFilt), name='OR')
    and_ = graphene.Field(graphene.List(lambda: newFilt), name="AND")

def _do_equals(field, value):
    print(value)
    print(field)
    return({"match":{field: {"query": value}}})

def _split_on_last_underscore(string):
    vals = string.split('___')
    return (("_".join(vals[0:len(vals)-1]),vals[-1]))

def parse_stuff(io):
    fields = io
    d = []
    for k, v in fields.items():
        (field, op) = _split_on_last_underscore(k)
        d.append(_do_equals(field, v))
    if(len(d)>1):
        return({"bool":{"must": d}})
    return d[0]
    
