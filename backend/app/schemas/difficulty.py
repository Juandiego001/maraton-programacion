from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto


class DifficultyIn(DefaultAuto):
    name = fields.String()
    value = fields.Integer()
    description = fields.String()
    status = fields.Boolean(required=False, load_default=True)


class DifficultyOut(DefaultAuto):
    name = fields.String()
    value = fields.Integer()
    description = fields.String()
    status = fields.Boolean()


class Difficulties(Schema):
    items = fields.List(fields.Nested(DifficultyOut))