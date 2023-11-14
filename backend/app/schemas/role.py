from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto, ObjectId


class RoleIn(DefaultAuto):
    name = fields.String()
    status = fields.Boolean()


class RoleOut(DefaultAuto):
    name = fields.String()
    status = fields.Boolean()


class Roles(Schema):
    items = fields.List(fields.Nested(RoleOut))