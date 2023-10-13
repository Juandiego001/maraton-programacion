from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto

class UserIn(DefaultAuto):
    name = fields.String()
    username = fields.String()
    email = fields.String()
    password = fields.String(required=False, load_default='')
    status = fields.String(load_default='PENDING', allow_none=True)

class UserOut(DefaultAuto):
    name = fields.String()
    username = fields.String()
    email = fields.String()
    status = fields.String()

class Users(Schema):
    items = fields.List(fields.Nested(UserOut))