from app.model import db
from datetime import datetime


class CommentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        return '<CommentGroup post_id: %d>' % self.post_id
