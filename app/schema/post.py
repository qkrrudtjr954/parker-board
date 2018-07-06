from marshmallow import ValidationError, validates_schema, pre_load
from flask_marshmallow.fields import fields
from app.model import db
from app.schema import ma
from app.model.post import Post
from app.schema.user import simple_user_schema

'''
스키마는 입력값 정제 vs 나가는값 정제

입력값 정제 : 필요한 스키마 만들어서 사용
출력값 정제 : 기본 스키마에서 only를 사용
'''


class PostSchema(ma.ModelSchema):
    user = fields.Nested(simple_user_schema)

    class Meta:
        strict = True
        model = Post
        sqla_session = db.session


simple_post_schema = PostSchema(only=['id', 'title'])

main_post_schema = PostSchema(only=['id', 'title', 'content', 'user', 'description', 'like_count', 'created_at', 'updated_at', 'read_count', 'comment_count'])
post_list_schema = PostSchema(only=['id', 'title', 'comment_count', 'created_at', 'user', 'read_count'], many=True)

post_id_schema = PostSchema(only=['id'])

post_like_count_schema = PostSchema(only=['like_count'])


class PostFormSchema(ma.ModelSchema):
    @validates_schema
    def post_create_validator(self, data):
        if 'title' not in data:
            raise ValidationError('게시글 제목을 입력해주세요', ['title'], status_code=422)

        if 'content' not in data:
            raise ValidationError('게시글 내용을 입력해주세요', ['content'], status_code=422)

        if len(data['title']) < 5:
            raise ValidationError('제목은 5글자 이상 입력해주세요', ['title'], status_code=422)

        if len(data['content']) < 20:
            raise ValidationError('내용은 20글자 이상 입력해주세요', ['content'], status_code=422)

    class Meta:
        strict = True
        model = Post
        sqla_session = db.session
        fields = ['title', 'content', 'description']


post_create_form_schema = PostFormSchema()
post_update_form_schema = PostFormSchema()
