from parker_board.schema import ma
from parker_board.model.user import User
from marshmallow import fields, ValidationError

import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class UserSchema(ma.ModelSchema):
    email = fields.Email()

    class Meta:
        strict = True
        model = User


user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True)



class SimpleUserSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String()


class LoginUserSchema(ma.Schema):
    email = fields.String()
    password = fields.String()


login_user_schema = LoginUserSchema(strict=True)
