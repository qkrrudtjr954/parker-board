import enum
from datetime import datetime
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

    def __repr__(self):
        return "<Comment id: %d, content: %s, status: %s" \
               " created_at: %s, updated_at: %s>"\
               % (self.id, self.content, self.status,
                  self.created_at, self.updated_at)

    def set_user_id(self, uid):
        self.user_id = uid

    def set_post_id(self, pid):
        self.post_id = pid

    def set_content(self, content):
        self.content = content

    def set_updated_at(self):
        self.updated_at = datetime.utcnow()

    def deleted(self):
        self.status = CommentStatus.DELETED