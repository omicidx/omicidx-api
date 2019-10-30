import graphene
import dateutil
import datetime
from graphql.language import ast
import typing
from ..esclient import ESClient

from ..mappings_stuff import FilterInputType
import app.mappings_stuff

SRA_STUDY_IDX = 'sra_study-zq'


class ESGraphqlDateTime(graphene.types.Scalar):
    """elasticsearch dates to GraphQL isoformat dates"""
    @staticmethod
    def serialize(dt):
        """convert an elasticsearch date to isoformat string date

        Parameters
        ----------
        dt: either a unix timestamp (int) or timestamp as a string
        
        Returns
        -------
        a string date in isoformat
        """
        # Two different date formats (unix timestamp=int, timestamp=string)
        # So, deal with both until sorted out on the elasticsearch side.
        try:
            return datetime.datetime.fromtimestamp(dt / 1000).isoformat()
        except:
            from dateutil import parser
            return parser.parse(dt).isoformat()

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return dateutil.parser.parse(node.value)

    @staticmethod
    def parse_value(value):
        return dateutil.parser.parse(value)


es = ESClient('config.ini').client


class AttributeType(graphene.ObjectType):
    class Meta:
        default_resolver = graphene.types.resolver.dict_resolver

    tag = graphene.String()
    value = graphene.String()


class XrefType(graphene.ObjectType):
    class Meta:
        default_resolver = graphene.types.resolver.dict_resolver

    id = graphene.String()
    db = graphene.String()


class IdentifierType(graphene.ObjectType):
    class Meta:
        default_resolver = graphene.types.resolver.dict_resolver

    id = graphene.String()
    namespace = graphene.String()
    uuid = graphene.String()


def return_basic_fields_from_index(idx):
    cls = idx
    fields = es.indices.get_mapping(idx)[cls]['mappings']['properties']
    short_fields = {}
    for name, details in fields.items():
        if (name == 'study'):
            short_fields[name] = graphene.Field(SRAStudyType)
        if (name == 'sample'):
            short_fields[name] = graphene.Field(SRASampleType)
        if ('type' not in details):
            continue

        if (details['type'] == 'text'):
            short_fields[name] = graphene.String()
        elif (details['type'] == 'boolean'):
            short_fields[name] = graphene.Boolean()
        elif (details['type'] == 'date'):
            short_fields[name] = ESGraphqlDateTime()
        elif (details['type'] == 'integer'):
            short_fields[name] = graphene.Int()
        elif (details['type'] == 'float'):
            short_fields[name] = graphene.Float()
        elif (details['type'] == 'nested' and name == 'attributes'):
            short_fields[name] = graphene.List(AttributeType,
                                               q=graphene.String())
        elif (details['type'] == 'nested' and name == 'identifiers'):
            short_fields[name] = graphene.List(IdentifierType)
        elif (details['type'] == 'nested' and name == 'xrefs'):
            short_fields[name] = graphene.List(XrefType, q=graphene.String())
        elif (details['type'] == 'nested' and name == 'runs'):
            short_fields[name] = graphene.List(SRARunType)
    import pprint
    return short_fields


class SRABase(graphene.Interface):
    totalCount = graphene.Int()


def createType(name, idx):
    short_fields = return_basic_fields_from_index(idx)
    return type(name, (graphene.ObjectType, ),
                short_fields,
                default_resolver=graphene.types.resolver.dict_resolver,
                interfaces=(SRABase, ))


def createType2(name, idx):
    short_fields = return_basic_fields_from_index(idx)
    return type(name, (graphene.ObjectType, ),
                short_fields,
                default_resolver=graphene.types.resolver.dict_resolver,
                interfaces=(SRABase, ))


SRAStudyType = createType('SRAStudyType', SRA_STUDY_IDX)
SRASampleType = createType('SRASampleType', 'sra_sample')
BiosampleType = createType('BiosampleType', 'biosample')
SRASampleType2 = createType2('SRASampleType2', 'sra_sample')
SRARunType = createType('SRARunType', 'sra_run')
SRAExperimentType = createType('SRAExperimentType', 'sra_experiment')


class SRARunConnection(graphene.relay.Connection):
    totalCount = graphene.Int()

    class Meta:
        node = SRARunType


class SRAExperimentConnection(graphene.relay.Connection):
    totalCount = graphene.Int()

    class Meta:
        node = SRAExperimentType


class IterableConnectionField2(graphene.Field):
    def __init__(self, type, *args, **kwargs):
        kwargs.setdefault("before", graphene.String())
        kwargs.setdefault("after", graphene.String())
        super().__init__(type, *args, **kwargs)


class M(graphene.InputObjectType):
    def __init__(self, fieldnames):
        self.enumfield = graphene.InputField(
            graphene.Enum(
                'Fields',
                list([(fieldname, fieldname) for fieldname in fieldnames])))
        self.field = graphene.InputField(graphene.String())


def get_by_accession(index, accession, doc_type='_doc'):
    res = es.get(index, doc_type=doc_type, id=accession)
    return res['_source']


# enumtest = graphene.Enum('enumtest',
#                          (('study', 'study'),
#                           ('study_accession', ['study.accession', 'abc'])))


def gen_input_field(cls, index):
    def resolver(parent,
                 info,
                 q: str = "*:*",
                 size: int = 50,
                 sort: typing.List[str] = ['_score', 'accession.keyword'],
                 aggs: typing.List[str] = []) -> object:
        body = {
            "sort": sort,
            "query": {
                "query_string": {
                    "query": q,
                    "fields": ["*"]
                }
            },
            "size": min(size, 500)
        }
        if (len(aggs) > 0):
            body['aggs'] = {}
            for f in aggs:
                body["aggs"][f] = {"terms": {"field": f + ".keyword"}}
        res = es.search(index, body=body)
        ret = []
        ret = list([x['_source'] for x in res['hits']['hits']])
        return ret

    return graphene.List(
        cls,
        resolver=resolver,
        description="query string query",
        q=graphene.String(required=False,
                          description="A query string that"
                          " follows the [lucene query string format]"
                          "(https://www.elastic.co/guide/en/elasticsearch"
                          "/reference/7.3/query-dsl-query-string-query."
                          "html#query-string-syntax)"),
        sort=graphene.List(graphene.String),
        size=graphene.Int(),
        aggs=graphene.List(graphene.String),
    )


def gen_get_by_accession(cls, index):
    def resolver(parent, info, accession):
        return get_by_accession(index, accession)

    return graphene.Field(
        cls,
        accession=graphene.String(description='Lookup by a single accession'),
        resolver=resolver)


class Query(graphene.ObjectType):
    """This is a test"""
    name = 'OmicIDX'
    description = 'query the omicidx'

    node = graphene.relay.Node.Field()

    sqlQuery = graphene.Field(
        graphene.String,
        query=graphene.String(description="elasticsearch sql query"),
        cursor=graphene.String(
            description="cursor for paging through sql results"))

    sqlTranslate = graphene.Field(
        graphene.JSONString,
        query=graphene.String(description="elasticsearch sql query"))
    sraStudyQuery = gen_input_field(SRAStudyType, SRA_STUDY_IDX)
    biosampleQuery = gen_input_field(BiosampleType, 'biosample')
    sraSampleQuery = gen_input_field(SRASampleType, 'sra_sample')
    sraRunQuery = gen_input_field(SRARunType, 'sra_run')
    sraExperimentQuery = gen_input_field(SRAExperimentType, 'sra_experiment')

    all_runs = IterableConnectionField2(SRARunConnection)

    sraStudy = gen_get_by_accession(SRAStudyType, SRA_STUDY_IDX)
    sraSample = gen_get_by_accession(SRASampleType, 'sra_sample')
    sraExperiment = gen_get_by_accession(SRAExperimentType, 'sra_experiment')
    sraRun = gen_get_by_accession(SRARunType, 'sra_run')

    def resolve_sqlQuery(root, info, query, cursor=None):
        if (cursor is not None):
            return es.transport.perform_request('post',
                                                '/_sql',
                                                body={"cursor": cursor})
        res = es.transport.perform_request('post',
                                           '/_sql',
                                           body={"query": query})
        return res

    def resolve_sqlTranslate(self, info, query):
        return es.transport.perform_request('post',
                                            '/_sql/translate/',
                                            body={"query": query})

    def resolve_sra_connection(self, connection_type, index, **args):
        filters = args.get('filter', {})
        first = args.get('first', 50)
        d = {}
        d['query'] = mappings_stuff.parse_stuff(filters)
        res = es.search('index', body={"query": q['body'], "size": first})
        ret = []
        return list([x['_source'] for x in res['hits']['hits']])
        #return(connection_type(
        #    page_info = graphene.relay.PageInfo(has_next_page=True, ),
        #    edges = list([connection_type.Edge(node=i, cursor='abc') for i in ret])))


schema = graphene.Schema(query=Query)
