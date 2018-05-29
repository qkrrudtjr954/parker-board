from parker_board.model.board import Board
from parker_board.schema import ma


class BoardSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Board


boards_schema = BoardSchema(many=True)
board_schema = BoardSchema()
