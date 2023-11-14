from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class UserIn(DefaultAuto):
    name = fields.String()
    username = fields.String()
    email = fields.String()
    roles = fields.List(ObjectId())
    password = fields.String(required=False, load_default='', allow_none=True)
    status = fields.String(required=False, load_default='PENDING')


class UserOut(DefaultAuto):
    name = fields.String()
    username = fields.String()
    email = fields.String()
    roles = fields.List(fields.String())
    status = fields.String()


class Users(Schema):
    items = fields.List(fields.Nested(UserOut))