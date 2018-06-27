from marshmallow import fields, validates, ValidationError, validates_schema
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

post_id_schema = PostSchema(only=['id'])


class PostCreateFormSchema(ma.ModelSchema):
    @validates_schema
    def post_title_length_check(self, data):
        if 'title' not in data:
            raise ValidationError('Post title can not be null.', 'title', status_code=422)

        if 'content' not in data:
            raise ValidationError('Post content can not be null.', 'content', status_code=422)

        if len(data['title']) < 5:
            raise ValidationError('Post title length mush more than 5.', status_code=422)

        if len(data['content']) < 20:
            raise ValidationError('Post content length mush more than 20.', status_code=422)

    class Meta:
        strict = True
        model = Post
        sqla_session = db.session
        fields = ['title', 'content', 'description']


post_create_form_schema = PostCreateFormSchema()


class PostUpdateFormSchema(ma.Schema):
    title = fields.String(200, missing=None, required=False)
    content = fields.String(2000, missing=None, required=False)
    description = fields.String(200, missing=None, required=False)

post_update_form_schema = PostUpdateFormSchema()
