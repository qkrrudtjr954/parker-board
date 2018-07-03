import re

from flask_marshmallow.fields import fields

from app.model import db
from app.schema import ma
from app.model.user import User, UserStatus
from marshmallow import ValidationError, validates_schema
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


simple_user_schema = UserSchema(only=['id', 'email'])
user_info_schema = UserSchema(only=['email'])

after_register_schema = UserSchema(only=['id', 'email', 'created_at'])
after_login_schema = UserSchema(only=['id', 'email'])


'''
로그인할때 유저의 email, password를 받는 스키마
- Validation이 필요함
'''

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


class UserFormSchema(ma.ModelSchema):
    @validates_schema
    def validate_length_check(self, data):
        if 'password' not in data:
            raise ValidationError('비밀번호를 입력해주세요', ['password'], status_code=422)
        if 'email' not in data:
            raise ValidationError('이메일을 입력해주세요', ['email'], status_code=422)
        if not EMAIL_REGEX.match(data['email']):
            raise ValidationError('올바른 이메일 형식이 아닙니다', ['email'], status_code=422)
        if len(data['password']) < 6:
            raise ValidationError('비밀번호는 6자 이상 입력해주세요', ['password'], status_code=422)

    class Meta:
        sqla_session = db.session
        strict = True
        model = User
        fields = ['email', 'password']


before_login_schema = UserFormSchema()
before_register_schema = UserFormSchema()


class IsLoggedInSchema(ma.Schema):
    is_logged_in = fields.Boolean(missing=False)


is_logged_in_schema = IsLoggedInSchema()