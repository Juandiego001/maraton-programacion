from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class SolutionIn(DefaultAuto):
    languageid = ObjectId()
    file = fields.File(required=False)
    link = fields.String()
    description = fields.String()
    judgment_status = fields.String()
    error = fields.String(required=False)
    status = fields.Boolean(required=False, load_default=True)


class SolutionOut(DefaultAuto):
    languageid = ObjectId()
    file_url = fields.String()
    link = fields.String()
    real_name = fields.String()
    hash_name = fields.String()
    description = fields.String()
    judgment_status = fields.String()
    error = fields.String()
    status = fields.Boolean()


class Solutions(Schema):
    items = fields.List(fields.Nested(SolutionOut))