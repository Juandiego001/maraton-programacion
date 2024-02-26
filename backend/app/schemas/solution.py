from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class SolutionIn(DefaultAuto):
    sourceid = ObjectId()
    topicsid = fields.List(ObjectId())
    structuresid = fields.List(ObjectId())
    file = fields.File(required=False)
    link = fields.String()
    description = fields.String()
    responseid = ObjectId()
    status = fields.Boolean(required=False, load_default=True)


class SolutionOut(DefaultAuto):
    contestid = ObjectId()
    challengeid = ObjectId()
    sourceid = ObjectId()
    topicsid = fields.List(ObjectId())
    structuresid = fields.List(ObjectId())
    file_url = fields.String()
    link = fields.String()
    real_name = fields.String()
    responseid = ObjectId()
    description = fields.String()
    status = fields.Boolean()


class SolutionsOut(DefaultAuto):
    full_contest = fields.String()
    full_challenge = fields.String()
    full_source = fields.String()
    full_response = fields.String()
    username = fields.String()
    file_url = fields.String()
    real_name = fields.String()
    link = fields.String()
    status = fields.Boolean()


class SolutionsQuery(Schema):
    contestid = ObjectId()
    challengeid = ObjectId()
    languageid = ObjectId()


class Solutions(Schema):
    items = fields.List(fields.Nested(SolutionsOut))
