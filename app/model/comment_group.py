from app import User
from app.model import db
from app.model.comment import Comment, CommentStatus
from datetime import datetime


class CommentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    comments = db.relationship('Comment', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<CommentGroup id: %d> ' % self.id

    def get_comment_in_group(self, comment_id):
        return self.comments.filter(~Comment.is_deleted).filter(Comment.id == comment_id).first()

    def add_comment(self, user, comment):
        try:
            comment.user_id = user.id

            self.comments.append(comment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            return comment

    def add_layer_comment(self, user: User, comment: Comment, parent_comment: Comment):
        try:
            self._update_comment_step(parent_comment)

            # add comment
            comment.user_id = user.id
            comment.step = parent_comment.step+1
            comment.depth = parent_comment.depth+1

            self.comments.append(comment)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            return comment

    def _update_comment_step(self, parent_comment: Comment):
        # update step
        self.comments \
            .filter(Comment.step > parent_comment.step) \
            .update({Comment.step: Comment.step + 1})