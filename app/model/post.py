import enum
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import ChoiceType

from app.model import db
from app.model.user import User
from app.model.comment import Comment


class PostStatus(enum.Enum):
    NORMAL = 0
    DELETED = 2


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(ChoiceType(PostStatus, impl=db.Integer()), default=PostStatus.NORMAL)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship("User")

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)

    comments = db.relationship("Comment", backref='post', lazy='dynamic')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_comments(self, page, per_page):
        return self.comments.filter(
            ~Comment.is_deleted
        ).order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    def refresh_update_time(self):
        self.updated_at = datetime.utcnow()

    @hybrid_property
    def is_deleted(self):
        return self.status == PostStatus.DELETED

    def deleted(self):
        self.status = PostStatus.DELETED

    def __repr__(self):
        return "<Post title: %s, content: %s, description: %s, status: %s," \
               " created_at: %s, updated_at: %s>"\
               % (self.title, self.content, self.description, self.status,
                  self.created_at, self.updated_at)

