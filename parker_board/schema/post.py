from marshmallow import fields
from parker_board.schema import ma
from parker_board.model.post import Post


class PostSchema(ma.ModelSchema):

    class Meta:
        strict = True
        model = Post


post_schema = PostSchema()
posts_schema = PostSchema(many=True)