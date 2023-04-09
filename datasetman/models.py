import datetime

from neomodel import (
    config,
    StructuredNode,
    StringProperty,
    IntegerProperty,
    UniqueIdProperty,
    RelationshipFrom,
    RelationshipTo,
    DateTimeProperty,
)
config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'


# Modelos Raven
class Dataset:
    def __init__(
        self, Id: str = None,  # type: ignore
        name: str = None,  # type: ignore
        description: str = None,  # type: ignore
        user_id: int = None,  # type: ignore
        upload_date: datetime.date = None  # type: ignore
    ):
        self.Id = Id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.upload_date = upload_date


# Modelos Neo4j
class Comment(StructuredNode):
    uid = UniqueIdProperty()
    content = StringProperty(required=True)
    user_id = IntegerProperty(required=True)
    dataset_id = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    replies = RelationshipTo('Reply', 'REPLY')


class Reply(StructuredNode):
    uid = UniqueIdProperty()
    content = StringProperty(required=True)
    user_id = IntegerProperty(required=True)
    parent_comment = RelationshipFrom(Comment, 'REPLY')
    created_at = DateTimeProperty(default_now=True)
