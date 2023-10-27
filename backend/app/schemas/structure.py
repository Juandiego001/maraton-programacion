from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto

class StructureIn(DefaultAuto):
    title = fields.String()
    description = fields.String()
    status = fields.Boolean(required=False, load_default=True)

class StructureOut(DefaultAuto):
    title = fields.String()
    description = fields.String()
    status = fields.Boolean()

class Structures(Schema):
    items = fields.List(fields.Nested(StructureOut))