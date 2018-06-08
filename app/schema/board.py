from app.model import db
from app.model.board import Board, BoardStatus
from app.schema import ma
from app.schema.user import simple_user_schema
from marshmallow import fields
from marshmallow_enum import EnumField


class BoardSchema(ma.ModelSchema):
    status = EnumField(BoardStatus)
    user = fields.Nested(simple_user_schema)

    class Meta:
        strict = True
        model = Board
        sqla_session = db.session


boards_schema = BoardSchema(many=True)
board_schema = BoardSchema()

after_fix_board_schema = BoardSchema(only=['id', 'description', 'title', 'created_at', 'user', 'status'])
after_del_board_schema = BoardSchema(only=['id', 'status', 'updated_at'])

main_board_schema = BoardSchema(only=['id', 'title', 'description', 'created_at'], many=True)