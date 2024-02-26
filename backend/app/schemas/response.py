from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto


class ResponseIn(DefaultAuto):
    code = fields.String()
    color = fields.String()
    description = fields.String()
    status = fields.Boolean(required=False, load_default=True)


class ResponseOut(DefaultAuto):
    code = fields.String()
    color = fields.String()
    description = fields.String()
    status = fields.Boolean()


class Responses(Schema):
    items = fields.List(fields.Nested(ResponseOut))