import elastic_graphene.converters as converters

import pytest


@pytest.fixture
@pytest.skip
def example_document():
    from elasticsearch_dsl import (
        Document, Keyword, Text,
        Date, InnerDoc, Nested, Object
    )
    
    class Comment(Document):
        author = Text(fields={'raw': Keyword()})
        content = Text(analyzer='snowball')
        created_at = Date()

        def age(self):
            return datetime.now() - self.created_at

    class Post(Document):
        author = Text()
        content = Text()
        created_at = Date()

        comments = Nested(Comment)

        co = Object(Comment)

    return Post()

@pytest.skip
def test_convert_elasticsearch_document(example_document):
    import graphene
    converted_document = converters.convert_elasticsearch_document(example_document)

    assert issubclass(converted_document, graphene.ObjectType)
    assert isinstance(converted_document.author, graphene.String)
    assert isinstance(converted_document.comments, graphene.List)
    assert issubclass(converted_document.co, graphene.ObjectType)

