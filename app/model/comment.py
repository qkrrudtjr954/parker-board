import enum
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import ChoiceType

from app.model import db
from app.model.user import User


class CommentStatus(enum.Enum):
    NORMAL = 0
    DELETED = 2


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    status = db.Column(ChoiceType(CommentStatus, impl=db.Integer()), default=CommentStatus.NORMAL)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def deleted(self):
        self.status = CommentStatus.DELETED
    @hybrid_property
    def is_deleted(self):
        return self.status == CommentStatus.DELETED

    def refresh_update_time(self):
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return "<Comment id: %d, content: %s, status: %s" \
               " created_at: %s, updated_at: %s>"\
               % (self.id, self.content, self.status,
                  self.created_at, self.updated_at)
