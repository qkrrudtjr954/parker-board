import enum
from datetime import datetime
from sqlalchemy_utils import ChoiceType

from app.model import db
from app.model.user import User
from app.model.post import Post


class BoardStatus(enum.Enum):
    NORMAL = 0
    DELETED = 2


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(ChoiceType(BoardStatus, impl=db.Integer()), default=BoardStatus.NORMAL)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")

    posts = db.relationship("Post", backref="board", lazy='dynamic')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_deleted(self):
        return True if self.status == BoardStatus.DELETED else False

    def deleted(self):
        self.status = BoardStatus.DELETED

    def get_posts(self, page, per_page):
        return self.posts\
            .filter(~Post.is_deleted)\
            .order_by(Post.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

    def refresh_update_time(self):
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return "<Board title: %s, description: %s, status: %s," \
               " created_at: %s, updated_at: %s>"\
               % (self.title, self.description, self.status,
                  self.created_at, self.updated_at)
