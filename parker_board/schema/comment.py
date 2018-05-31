from parker_board.schema import ma
from parker_board.model.comment import Comment
from marshmallow import fields
from parker_board.schema.user import CommentUserSchema


class CommentSchema(ma.ModelSchema):
    user = fields.Nested(CommentUserSchema())

    class Meta:
        strict = True
        model = Comment


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
