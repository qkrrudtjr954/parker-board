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
'''
스키마는 입력값 정제 vs 나가는값 정제

입력값 정제 : 필요한 스키마 만들어서 사용
출력값 정제 : 기본 스키마에서 only를 사용
'''


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


simple_post_schema = ExtensionPostSchema(only=['id', 'title'])

main_post_schema = ExtensionPostSchema(only=['id', 'title', 'content', 'comments_count', 'created_at', 'user', 'description', 'updated_at'])
post_list_schema = ExtensionPostSchema(only=['id', 'title', 'comments_count', 'created_at', 'user'])

after_create_post_schema = ExtensionPostSchema(only=['id', 'title', 'content', 'description', 'created_at', 'user'])
after_update_post_schema = ExtensionPostSchema(only=['id', 'title', 'content', 'description', 'created_at', 'user'])
after_delete_post_schema = ExtensionPostSchema(only=['id', 'title', 'status'])


class PostFormSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Post
        sqla_session = db.session
        fields = ['title', 'content', 'description']


before_create_post_schema = PostFormSchema()
before_update_post_schema = PostFormSchema()
