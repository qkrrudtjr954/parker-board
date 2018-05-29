from parker_board.schema import ma
from parker_board.model.comment import Comment


class CommentSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Comment


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
