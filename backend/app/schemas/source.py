from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class SourceIn(Schema):
    challengeid = ObjectId()
    languageid = ObjectId()


class SourceOut(Schema):
    challengeid = ObjectId()
    languageid = ObjectId()
    full_source = fields.String()


class Sources(Schema):
    items = fields.List(fields.Nested(SourceOut))