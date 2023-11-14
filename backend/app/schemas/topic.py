from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto


class TopicIn(DefaultAuto):
    title = fields.String()
    description = fields.String()
    status = fields.Boolean(required=False, load_default=True)


class TopicOut(DefaultAuto):
    title = fields.String()
    description = fields.String()
    status = fields.Boolean()


class Topics(Schema):
    items = fields.List(fields.Nested(TopicOut))