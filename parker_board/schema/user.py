from parker_board.schema import ma
from parker_board.model.user import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User