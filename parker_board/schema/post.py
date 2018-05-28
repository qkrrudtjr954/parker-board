from marshmallow import fields
from parker_board.schema import ma
from parker_board.model.post import Post


class PostSchema(ma.ModelSchema):
    # id = fields.Integer(dump_only=True)
    # title = fields.String(required=True)
    # content = fields.String(required=True)
    # description = fields.String(required=True)
    # status = fields.Integer(dump_only=True)
    #
    # user_id = fields.Integer(required=True)
    # board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    # # comments = db.relationship('Comment', backref='post', lazy=True)
    #
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    class Meta:
        strict=True
        model = Post


post_schema = PostSchema()
posts_schema = PostSchema(many=True)