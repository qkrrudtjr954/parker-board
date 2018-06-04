from marshmallow import fields, post_dump
from parker_board.schema import ma
from parker_board.model.post import Post
from parker_board.schema.comment import CommentSchema
from parker_board.schema.user import SimpleUserSchema


class PostSchema(ma.ModelSchema):
    user = fields.Nested(SimpleUserSchema())
    comments = fields.List(fields.Nested(CommentSchema()))
    comments_count = fields.Integer(missing=0, dump_only=True)

    @post_dump
    def count(self, data):
        data['comments_count'] = len(data['comments'])
        return data

    class Meta:
        strict = True
        model = Post


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