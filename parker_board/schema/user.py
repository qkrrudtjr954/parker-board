from parker_board.schema import ma
from parker_board.model.user import User


class UserSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)