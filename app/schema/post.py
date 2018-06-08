from marshmallow import fields, post_dump

from app.model import db
from app.schema import ma
from app.model.post import Post
from app.schema.comment import CommentSchema
from app.schema.user import simple_user_schema


class PostSchema(ma.ModelSchema):
    user = fields.Nested(simple_user_schema)
    comments = fields.List(fields.Nested(CommentSchema()))
    comments_count = fields.Integer(missing=0, dump_only=True)

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



class SimplePostSchema(ma.ModelSchema):
    comments_count = fields.Integer(missing=0, dump_only=True)

    @post_dump
    def count(self, data):
        data['comments_count'] = len(data['comments'])
        return data

    @post_dump
    def description_length(self, data):
        desc = data['description']
        if desc and len(desc)> 15:
            data['description'] = desc[0:10]+'...'

    @post_dump
    def content_length(self, data):
        con = data['content']
        if con and len(con) > 30:
            data['content'] = con[0:10] + '...'

    class Meta:
        strict = True
        model = Post


simple_posts_schema = SimplePostSchema(many=True)

