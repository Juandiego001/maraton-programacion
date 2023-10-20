from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId

class RoleIn(DefaultAuto):
    name = fields.String()
    status = fields.Boolean()

class RoleOut(DefaultAuto):
    name = fields.String()
    status = fields.Boolean()

class RoleUserOut(Schema):
    _id = ObjectId()
    name = fields.String()

class Roles(Schema):
    items = fields.List(fields.Nested(RoleOut))