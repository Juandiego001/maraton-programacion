from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class SolutionIn(DefaultAuto):
    sourceid = ObjectId()
    file = fields.File(required=False)
    link = fields.String()
    description = fields.String()
    judgment_status = fields.String()
    error = fields.String(required=False)
    status = fields.Boolean(required=False, load_default=True)


class SolutionOut(DefaultAuto):
    contestid = ObjectId()
    challengeid = ObjectId()
    sourceid = ObjectId()
    file_url = fields.String()
    link = fields.String()
    real_name = fields.String()
    judgment_status = fields.String()
    error = fields.String()
    description = fields.String()
    status = fields.Boolean()


class SolutionsOut(DefaultAuto):
    full_contest = fields.String()
    full_challenge = fields.String()
    full_source = fields.String()
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
