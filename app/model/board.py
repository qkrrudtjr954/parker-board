import enum
from datetime import datetime

from sqlalchemy_utils import ChoiceType

from app.model import db
from app.model.post import Post


class BoardStatus(enum.Enum):
    NORMAL = 0
    DELETED = 2


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(ChoiceType(BoardStatus), default=BoardStatus.NORMAL)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")

    posts = db.relationship("Post", back_populates="board")
    # posts = db.relationship('Post', backref='board', lazy=True, primaryjoin='and_(Board.id == Post.board_id, Post.status != 2)')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Board id: %d, title: %s, description: %s, status: %d," \
               " created_at: %s, updated_at: %s>"\
               % (self.id, self.title, self.description, self.status,
                  self.created_at, self.updated_at)

    def set_user_id(self, uid):
        self.user_id = uid

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_updated_at(self):
        self.updated_at = datetime.utcnow()

    def deleted(self):
        self.status = BoardStatus.DELETED
