from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId
from app.schemas.contest import ContestChallengeOut
from app.schemas.topic import TopicOut


class ChallengeIn(DefaultAuto):
    title = fields.String()
    source = fields.String()
    contestid = ObjectId()
    topicsid = fields.List(ObjectId(), required=False)
    difficulty = fields.String(required=False, load_default='EASY')
    status = fields.Boolean(required=False)


class ChallengeOut(DefaultAuto):
    title = fields.String()
    source = fields.String()
    contestid = ObjectId()
    topicsid = fields.List(ObjectId(), required=False)
    difficulty = fields.String()
    contest = fields.Nested(ContestChallengeOut)
    topics = fields.List(fields.Nested(TopicOut))
    full_challenge = fields.Function(
        lambda challenge: f'{challenge["title"]} - \
            {challenge["contest"]["full_contest"]}')
    status = fields.Boolean()


class Challenges(Schema):
    items = fields.List(fields.Nested(ChallengeOut))
