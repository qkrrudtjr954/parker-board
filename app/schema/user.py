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

after_leave_schema = UserSchema(only=['id', 'email', 'created_at', 'updated_at', 'status'])

simple_user_schema = UserSchema(only=['id', 'email'])

login_schema = UserSchema(strict=True, only=['email', 'password'])



'''
로그인할때 유저의 email, password를 받는 스키마
- Validation이 필요함
'''
class UserFormSchema(ma.ModelSchema):
    email = fields.Email()
    password = fields.String()

    @validates('password')
    def validate_length_check(self, pwd):
        if len(pwd) < 5:
            raise ValidationError('Password too short', status_code=422)

    class Meta:
        sqla_session = db.session
        strict = True
        model = User
        fields = ('email', 'password', 'created_at', 'updated_at')


before_login_schema = UserFormSchema()
before_register_schema = UserFormSchema()


class UserInfoSchema(ma.ModelSchema):
    class Meta:
        sqla_session = db.session
        strict = True
        model = User
        exclude = ['status']


after_register_schema = UserInfoSchema(only=['id', 'email', 'created_at'])
after_login_schema = UserInfoSchema(only=['id', 'email', 'status'])