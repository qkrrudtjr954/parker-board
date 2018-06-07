from app.schema import ma
from app.model.user import User
from marshmallow import fields, ValidationError, validates


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
    password = fields.String()

    @validates('password')
    def validate_length_check(self, pwd):
        if len(pwd) < 5:
            raise ValidationError('Password too short', status_code=422)


login_schema = LoginUserSchema(strict=True)