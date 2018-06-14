from marshmallow import fields
from marshmallow_enum import EnumField
from app.model import db
from app.model.comment import CommentStatus
from app.schema import ma
from app.model.post import Post, PostStatus
from app.schema.user import simple_user_schema
from app.schema.board import simple_board_schema


'''
스키마는 입력값 정제 vs 나가는값 정제

입력값 정제 : 필요한 스키마 만들어서 사용
출력값 정제 : 기본 스키마에서 only를 사용
'''


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


simple_post_schema = PostSchema(only=['id', 'title'])

main_post_schema = PostSchema(only=['id', 'title', 'content', 'comments_count', 'created_at', 'user', 'description', 'updated_at'])
post_list_schema = PostSchema(only=['id', 'title', 'comments_count', 'created_at', 'user'], many=True)

post_redirect_schema = PostSchema(only=['id'])


class PostFormSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Post
        sqla_session = db.session
        fields = ['title', 'content', 'description']


post_create_form_schema = PostFormSchema()
post_update_form_schema = PostFormSchema()




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