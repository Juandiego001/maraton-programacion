from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class MaterialIn(DefaultAuto):
    file = fields.File(required=False)
    link = fields.String()
    status = fields.Boolean(required=False, load_default=True)


class MaterialOut(DefaultAuto):
    file_url = fields.String()
    link = fields.String()
    real_name = fields.String()
    status = fields.Boolean()


class Materials(Schema):
    items = fields.List(fields.Nested(MaterialOut))