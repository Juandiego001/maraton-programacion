from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId

class ContestIn(DefaultAuto):
    platform = fields.String()
    made_at = fields.String()
    name = fields.String(required=False)
    file_url = fields.String(required=False)
    status = fields.Boolean(required=False, load_default=True)

class ContestOut(DefaultAuto):
    platform = fields.String()
    made_at = fields.String()
    name = fields.String()
    file_url = fields.String()
    status = fields.String()

class ContestChallengeOut(Schema):
    _id = ObjectId()
    full_contest = fields.String()

class Contests(Schema):
    items = fields.List(fields.Nested(ContestOut))