from marshmallow import fields
from parker_board.schema import ma
from marshmallow import ValidationError


def validate_password(pwd):
    if len(pwd) < 6:
        raise ValidationError('Password is too short', status_code=422)


class LoginReqSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(validate=validate_password, required=True)

    class Meta:
        strict=True
        fields = ('email', 'password')


login_req_schema = LoginReqSchema()