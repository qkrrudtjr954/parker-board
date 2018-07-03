from flask_marshmallow.fields import fields
from app.schema import ma


class LikeSchema(ma.Schema):
    is_liked = fields.Boolean()


is_liked_schema = LikeSchema()