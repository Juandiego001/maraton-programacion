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
    contestid = ObjectId()
    languagesid = fields.List(ObjectId())
    topicsid = fields.List(ObjectId(), required=False)
    difficultyid = ObjectId()
    contest = fields.Nested(ContestChallengeOut)
    topics = fields.List(fields.Nested(TopicOut))
    full_challenge = fields.Function(
        lambda challenge: f'{challenge["title"]} - \
            {challenge["contest"]["full_contest"]}')
    status = fields.Boolean()


class Challenges(Schema):
    items = fields.List(fields.Nested(ChallengeOut))
