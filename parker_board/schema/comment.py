from marshmallow import fields
from parker_board.schema import ma
from parker_board.model.comment import Comment


class CommentSchema(ma.ModelSchema):
    content = fields.String(required=True)

    class Meta:
        model = Comment


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
