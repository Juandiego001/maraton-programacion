from apiflask import Schema, fields
import bson
from marshmallow import EXCLUDE, ValidationError, missing
from apiflask.validators import Length
from datetime import datetime


class ObjectId(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return bson.ObjectId(value)
        except Exception:
            raise ValidationError(f'Invalid ObjectId {value}')

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        return str(value)


class DateField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return datetime.fromisoformat(value)
        except Exception:
            raise ValidationError(f'Invalid datetime object {value}')

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        if type(value) is str:
            return str(datetime.fromisoformat(value).date())
        if type(value) is datetime:
            return value.date()
        return str(value)


class DefaultAuto(Schema):

    class Meta:
        unknown = EXCLUDE

    _id = ObjectId(dump_only=True)
    updated_by = fields.String(dump_only=True, validate=[Length(0, 100)])
    updated_at = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)


class Message(Schema):
    message = fields.String()
    data = fields.Dict()
