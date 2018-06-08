from app.model import db
from app.schema import ma
from app.model.user import User, UserStatus
from marshmallow import fields, ValidationError, validates
from marshmallow_enum import EnumField


class UserSchema(ma.ModelSchema):
    email = fields.Email()
    status = EnumField(UserStatus)

    @validates('password')
    def validate_length_check(self, pwd):
        if len(pwd) < 5:
            raise ValidationError('Password too short', status_code=422)

    class Meta:
        sqla_session = db.session
        strict = True
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)

after_register_schema = UserSchema(only=['id', 'email', 'created_at'])
after_login_schema = UserSchema(only=['id', 'email', 'status'])
after_leave_schema = UserSchema(only=['id', 'email', 'created_at', 'updated_at', 'status'])

simple_user_schema = UserSchema(only=['id', 'email'])


class LoginSchema(ma.Schema):
    email = fields.Email()
    password = fields.String()

    @validates('password')
    def validate_length_check(self, pwd):
        if len(pwd) < 5:
            raise ValidationError('Password too short', status_code=422)

login_schema = LoginSchema(strict=True)
