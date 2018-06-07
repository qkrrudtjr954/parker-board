from app.schema import ma
from app.model.comment import Comment
from marshmallow import fields
from app.schema.user import SimpleUserSchema


class CommentSchema(ma.ModelSchema):
    user = fields.Nested(SimpleUserSchema())

    class Meta:
        strict = True
        model = Comment


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
