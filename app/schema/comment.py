from marshmallow import fields, validates, ValidationError
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


comment_list_schema = CommentSchema(only=['id', 'user', 'content', 'created_at'], many=True)

after_create_schema = CommentSchema(only=['id', 'created_at'])  # comment 가 생성되면 id, create_at 만 내려줌, 다른 정보는 이미 존재함
after_updated_schema = CommentSchema(only=['id', 'updated_at'])


class CommentFormSchema(ma.ModelSchema):
    @validates('content')
    def content_length_check(self, content):
        if not content:
            raise ValidationError('내용을 입력해주세요', status_code=422)
        if len(content) < 10:
            raise ValidationError('내용은 10글자 이상 입력해주세요', status_code=422)

    class Meta:
        strict = True
        model = Comment
        sqla_session = db.session
        fields = ['content']


comment_create_form_schema = CommentFormSchema()
comment_update_form_schema = CommentFormSchema()


class LayerCommentFormSchema(ma.ModelSchema):
    @validates('content')
    def content_length_check(self, content):
        if not content:
            raise ValidationError('내용을 입력해주세요', status_code=422)
        if len(content) < 10:
            raise ValidationError('내용은 10글자 이상 입력해주세요', status_code=422)

    class Meta:
        strict = True
        model = Comment
        sqla_session = db.session
        fields = ['content', 'parent_id']

layer_comment_create_form = LayerCommentFormSchema()
