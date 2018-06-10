from marshmallow import fields
from marshmallow_enum import EnumField
from app.model import db
from app.model.comment import Comment, CommentStatus
from app.schema import ma
from app.schema.user import simple_user_schema


class CommentSchema(ma.ModelSchema):
    user = fields.Nested(simple_user_schema)
    status = EnumField(CommentStatus)

    class Meta:
        strict = True
        model = Comment
        sqla_session = db.session


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
