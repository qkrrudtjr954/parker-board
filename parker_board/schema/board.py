from marshmallow import fields
from parker_board.model.board import Board
from parker_board.schema import ma


class BoardSchema(ma.ModelSchema):
    title = fields.String(required=True)
    description = fields.String(required=False)

    class Meta:
        strict=True
        model = Board


boards_schema = BoardSchema(many=True)
board_schema = BoardSchema()



class PatchBoardSchema(ma.Schema):
    title = fields.String(required=False)
    description = fields.String(required=False)

    class Meta:
        strict = True


patch_board_schema = PatchBoardSchema()