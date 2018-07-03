from app.model import db
from .timestamp import TimestampMixin


class Likes(TimestampMixin, db.Model):
    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
