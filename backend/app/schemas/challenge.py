from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId
from app.schemas.contest import ContestChallengeOut
from app.schemas.topic import TopicOut


class ChallengeIn(DefaultAuto):
    title = fields.String()
    name = fields.String()
    contestid = ObjectId()
    languagesid = fields.List(ObjectId())
    topicsid = fields.List(ObjectId(), required=False)
    difficultyid = ObjectId()
    status = fields.Boolean(required=False)


class ChallengeOut(DefaultAuto):
    title = fields.String()
    name = fields.String()    
    status = fields.Boolean()
    contestid = ObjectId()
    full_contest = fields.String()
    contest_url = fields.String()
    contest_link = fields.String()
    languagesid = fields.List(ObjectId())
    topicsid = fields.List(ObjectId())
    difficultyid = ObjectId()
    status = fields.Boolean()


class Challenges(Schema):
    items = fields.List(fields.Nested(ChallengeOut))
