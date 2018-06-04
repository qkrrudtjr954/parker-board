from parker_board.schema import ma
from parker_board.model.user import User
from marshmallow import fields, ValidationError

class UserSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = User


user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True)



class SimpleUserSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String()


def password_length_check(pwd):
    print(pwd+'asdf')
    if len(pwd) < 5:
        raise ValidationError('Password too short', code=422)

class LoginUserSchema(ma.Schema):
    email = fields.Email()
    password = fields.String(validate=password_length_check)


login_schema = LoginUserSchema(strict=True)