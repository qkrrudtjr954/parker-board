from marshmallow import fields, post_dump
from parker_board.schema import ma
from parker_board.model.post import Post
from parker_board.schema.comment import CommentSchema


class PostSchema(ma.ModelSchema):
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