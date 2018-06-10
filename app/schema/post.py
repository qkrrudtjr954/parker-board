from marshmallow import fields, post_dump
from marshmallow_enum import EnumField
from app.model import db
from app.model.comment import Comment, CommentStatus
from app.schema import ma
from app.model.post import Post, PostStatus
from app.schema.user import simple_user_schema
from app.schema.board import simple_board_schema


class PostSchema(ma.ModelSchema):
    board = fields.Nested(simple_board_schema)
    user = fields.Nested(simple_user_schema)

    comments_count = fields.Method('get_comments_count')

    status = EnumField(PostStatus)

    def get_comments_count(self, obj):
        comments = [c for c in obj.comments if c.status != CommentStatus.DELETED]
        return len(comments)

    class Meta:
        strict = True
        model = Post
        sqla_session = db.session


post_schema = PostSchema()

main_posts_schema = PostSchema(many=True, only=['id', 'title', 'content', 'comments_count', 'created_at', 'user', 'description'])
main_post_schema = PostSchema(only=['id', 'title', 'content', 'comments_count', 'created_at', 'user', 'description'])
simple_post_schema = PostSchema(only=['id', 'title'])

