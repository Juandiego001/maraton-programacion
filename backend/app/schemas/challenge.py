from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId
from app.schemas.contest import ContestChallengeOut
from app.schemas.topic import TopicOut

class ChallengeIn(DefaultAuto):
    title = fields.String()
    source = fields.String()
    contestid = ObjectId()
    topicsid = fields.List(ObjectId(), required=False)
    status = fields.Boolean(required=False)

class ChallengeOut(DefaultAuto):
    title = fields.String()
    source = fields.String()
    contest = fields.Nested(ContestChallengeOut)
    topics = fields.List(fields.Nested(TopicOut))
    status = fields.Boolean()

class Challenges(Schema):
    items = fields.List(fields.Nested(ChallengeOut))