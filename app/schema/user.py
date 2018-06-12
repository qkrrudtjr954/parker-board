from app.model import db
from app.schema import ma
from app.model.user import User, UserStatus
from marshmallow import fields, ValidationError, validates
from marshmallow_enum import EnumField


'''
스키마는 입력값 정제 vs 나가는값 정제

입력값 정제 : 필요한 스키마 만들어서 사용
출력값 정제 : 기본 스키마에서 only를 사용
'''


class UserSchema(ma.ModelSchema):
    status = EnumField(UserStatus)
    class Meta:
        sqla_session = db.session
        strict = True
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)

simple_user_schema = UserSchema(only=['id', 'email'])

after_leave_schema = UserSchema(only=['id', 'email', 'created_at', 'updated_at', 'status'])
after_register_schema = UserSchema(only=['id', 'email', 'created_at'])
after_login_schema = UserSchema(only=['id', 'email'])


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
        fields = ['email', 'password']


before_login_schema = UserFormSchema()
before_register_schema = UserFormSchema()
