from app.model import db
from app.schema import ma
from app.model.comment import Comment
from marshmallow import fields
from app.schema.user import simple_user_schema


class CommentSchema(ma.ModelSchema):
    user = fields.Nested(simple_user_schema)

    class Meta:
        strict = True
        model = Comment
        sqla_session = db.session


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
