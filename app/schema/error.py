from flask_marshmallow.fields import fields

from app.schema import ma


class ErrorSchema(ma.Schema):
    messages = fields.Dict()
    message = fields.String(255)


default_messages_error_schema = ErrorSchema(only=['messages'])
default_message_error_schema = ErrorSchema(only=['message'])

