from parker_board.schema import ma
from parker_board.model.user import User
from marshmallow import fields

class UserSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = User


user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True)



class SimpleUserSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String()


class LoginUserSchema(ma.Schema):
    email = fields.Email()
    password = fields.String(lambda pwd : len(pwd) > 6)


login_schema = LoginUserSchema()