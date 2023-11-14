from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class ContestIn(DefaultAuto):
    platform = fields.String()
    made_at = fields.String()
    name = fields.String(required=False)
    file_url = fields.String(required=False)
    link = fields.String(required=False)
    isTraining = fields.Boolean(required=False, load_default=False)
    status = fields.Boolean(required=False, load_default=True)


class ContestOut(DefaultAuto):
    platform = fields.String()
    made_at = fields.String()
    name = fields.String()
    file_url = fields.String()
    link = fields.String()
    isTraining = fields.Boolean()
    status = fields.String()
    full_contest = fields.Function(
        lambda contest: f'{contest["platform"]} {contest["made_at"]}')


class ContestChallengeOut(Schema):
    _id = ObjectId()
    full_contest = fields.String()


class Contests(Schema):
    items = fields.List(fields.Nested(ContestOut))