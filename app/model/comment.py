import enum

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import ChoiceType

from app.model import db
from app.model.timestamp import TimestampMixin
from app.model.user import User


class CommentStatus(enum.Enum):
    NORMAL = 0
    DELETED = 2


class Comment(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(ChoiceType(CommentStatus, impl=db.Integer()), default=CommentStatus.NORMAL)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")

    comment_group_id = db.Column(db.Integer, db.ForeignKey('comment_group.id'), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    depth = db.Column(db.Integer, nullable=False, default=0)
    step = db.Column(db.Integer, nullable=False, default=0)

    edited_count = db.Column(db.Integer, default=0)

    def delete(self):
        self.comment_group.post.decrease_comment_count()
        self.status = CommentStatus.DELETED

        db.session.commit()

    @hybrid_property
    def is_deleted(self):
        return self.status == CommentStatus.DELETED

    def is_owner(self, user: User):
        return self.user_id == user.id

    def update(self, data):
        self.content = data
        self.edited_count = Comment.edited_count + 1

        db.session.commit()

    def __repr__(self):
        return "<Comment content: %s, status: %s" \
               " created_at: %s, updated_at: %s>"\
               % (self.content, self.status,
                  self.created_at, self.updated_at)
