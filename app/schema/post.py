from marshmallow import fields, post_dump
from marshmallow_enum import EnumField
from app.model import db
from app.schema import ma
from app.model.post import Post, PostStatus
from app.schema.comment import CommentSchema
from app.schema.user import simple_user_schema
from app.schema.board import simple_board_schema


class PostSchema(ma.ModelSchema):
    board = fields.Nested(simple_board_schema)
    user = fields.Nested(simple_user_schema)
    comments = fields.List(fields.Nested(CommentSchema()))
    comments_count = fields.Integer(missing=0, dump_only=True)
    status = EnumField(PostStatus)

    @post_dump
    def count(self, data):
        data['comments_count'] = len(data['comments'])
        return data

    class Meta:
        strict = True
        model = Post
        sqla_session = db.session


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

main_post_schema = PostSchema(many=True, only=['id', 'title', 'content', 'comments', 'comments_count', 'created_at', 'user'])