from app.model.board import Board
from app.schema import ma
from marshmallow import fields
from app.schema.user import simple_user_schema


class BoardSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Board


boards_schema = BoardSchema(many=True)
board_schema = BoardSchema()


class MainBoardSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(200)
    user = fields.Nested(simple_user_schema)
    description = fields.String()
    created_at = fields.DateTime()


main_boards_schema = MainBoardSchema(many=True)