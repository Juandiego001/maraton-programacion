from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId, DateField


class ContestIn(DefaultAuto):
    platform = fields.String()
    made_at = DateField()
    name = fields.String(required=False)
    file = fields.File(required=False)
    link = fields.String(required=False)
    isTraining = fields.Boolean(required=False, load_default=False)
    status = fields.Boolean(required=False, load_default=True)


class ContestOut(DefaultAuto):
    platform = fields.String()
    made_at = DateField()
    name = fields.String()
    file_url = fields.String()
    real_name = fields.String()
    link = fields.String()
    isTraining = fields.Boolean()
    status = fields.String()
    full_contest = fields.Function(
        lambda contest: f'{contest["platform"]} {contest["made_at"]}')


class ContestChallengeOut(Schema):
    _id = ObjectId()
    full_contest = fields.String()


class ContestsQuery(Schema):
    platform = fields.String()
    name = fields.String()
    isTraining = fields.Boolean()
    initial_date = DateField()
    end_date = DateField()


class Contests(Schema):
    items = fields.List(fields.Nested(ContestOut))