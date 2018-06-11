from marshmallow import fields, post_dump
from marshmallow_enum import EnumField
from app.model import db
from app.model.comment import Comment, CommentStatus
from app.schema import ma
from app.model.post import Post, PostStatus
from app.schema.user import simple_user_schema
from app.schema.board import simple_board_schema


# class PostSchema(ma.ModelSchema):
#     class Meta:
#         strict = True
#         model = Post
#         sqla_session = db.session
#
#
# class PostInListSchema(PostSchema):
#     board = fields.Nested(simple_board_schema)
#     user = fields.Nested(simple_user_schema)
#
#     comments_count = fields.Method('get_comments_count')
#
#     def get_comments_count(self, obj):
#         comments = [c for c in obj.comments if c.status != CommentStatus.DELETED]
#         return len(comments)


# post_write_schema = PostSchema(only=['title', 'content'])
# post_update_schema = PostSchema(only=['title', 'content'])
#
#
# post_form_schema = PostSchema(only=['title', 'content'])
#
#
# class PostFormSchema(ma.Schema):
#     title = fields.String()
#     content = fields.String()
#
#

class DefaultPostSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Post
        sqla_session = db.session


class ExtensionPostSchema(DefaultPostSchema):
    board = fields.Nested(simple_board_schema)
    user = fields.Nested(simple_user_schema)

    comments_count = fields.Method('get_comments_count')

    status = EnumField(PostStatus)

    def get_comments_count(self, obj):
        comments = [c for c in obj.comments if c.status != CommentStatus.DELETED]
        return len(comments)


post_schema = ExtensionPostSchema()

main_posts_schema = ExtensionPostSchema(many=True, only=['id', 'title', 'content', 'comments_count', 'created_at', 'user', 'description'])
main_post_schema = ExtensionPostSchema(only=['id', 'title', 'content', 'comments_count', 'created_at', 'user', 'description'])
simple_post_schema = ExtensionPostSchema(only=['id', 'title'])


# post list 에서 필요한 스키마
# id, title, description, created_at, updated_at, comment_count, user
class PostListSchema(ma.ModelSchema):
    user = fields.Nested(simple_user_schema)
    comments_count = fields.Method('get_comments_count')

    def get_comments_count(self, obj):
        comments = [c for c in obj.comments if c.status != CommentStatus.DELETED]
        return len(comments)

    class Meta:
        strict = True
        model = Post
        sql_session = db.session
        exclude = ['content', 'status', 'comments', 'board']


post_list_schema = PostListSchema(many=True)



class PostFormSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Post
        sqla_session = db.session
        fields = ['title', 'content']

before_create_post_schema = PostFormSchema()
