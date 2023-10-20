from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto

class PermissionIn(DefaultAuto):
    slug = fields.String()
    action = fields.String()
    status = fields.Boolean()

class PermissionOut(DefaultAuto):
    slug = fields.String()
    action = fields.String()
    status = fields.Boolean()

class Permissions(Schema):
    items = fields.List(fields.Nested(PermissionOut))