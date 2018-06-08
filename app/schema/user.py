from app.model import db
from app.schema import ma
from app.model.user import User
from marshmallow import fields, ValidationError, validates


class UserSchema(ma.ModelSchema):
    email = fields.Email()

    @validates('password')
    def validate_length_check(self, pwd):
        if len(pwd) < 5:
            raise ValidationError('Password too short', status_code=422)

    class Meta:
        strict = True
        model = User
        sqla_session = db.session


user_schema = UserSchema()
users_schema = UserSchema(many=True)

after_register_schema = UserSchema(only=['id', 'email', 'created_at'])
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
