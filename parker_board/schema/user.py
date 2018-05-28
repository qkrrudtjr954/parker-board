from marshmallow import fields, ValidationError
from parker_board.schema import ma
from parker_board.model.user import User


class UserSchema(ma.ModelSchema):
    email = fields.Email(required=True)
    class Meta:
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)