from apiflask import Schema, fields
from app.schemas.generic import DefaultAuto


class Login(Schema):
    password = fields.String()
    username = fields.String()

class ChangePassword(Schema):
    new_password = fields.String()
    current_password = fields.String()

class Email(Schema):
    email = fields.String()

class NewPassword(Schema):
    new_password = fields.String()

class Ability(Schema):
    subject = fields.String()
    action = fields.String()

class Profile(DefaultAuto):
    abilities = fields.List(fields.Nested(Ability))
    username = fields.String()
    name = fields.String()
    lastname = fields.String()
    document = fields.Integer()
    email = fields.String()

class Photo(Schema):
    photo = fields.File()

