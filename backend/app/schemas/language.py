from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto


class LanguageIn(DefaultAuto):
    name = fields.String()
    description = fields.String()
    status = fields.Boolean(required=False, load_default=True)


class LanguageOut(DefaultAuto):
    name = fields.String()
    description = fields.String()
    status = fields.Boolean()


class Languages(Schema):
    items = fields.List(fields.Nested(LanguageOut))