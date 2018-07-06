from app.model import db
from app.model.comment import Comment
from datetime import datetime


class CommentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    comments = db.relationship('Comment', backref='group')

    def __repr__(self):
        return '<CommentGroup id: %d> ' % self.id
