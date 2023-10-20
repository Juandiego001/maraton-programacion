from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId
from app.schemas.role import RoleUserOut

class UserIn(DefaultAuto):
    name = fields.String()
    username = fields.String()
    email = fields.String()
    password = fields.String(required=False, load_default='')
    roles = fields.List(fields.String(required=False), required=False, load_default=[])
    status = fields.String(required=False)

class UserOut(DefaultAuto):
    name = fields.String()
    username = fields.String()
    email = fields.String()
    roles = fields.List(fields.Nested(RoleUserOut))
    status = fields.String()

class Users(Schema):
    items = fields.List(fields.Nested(UserOut))