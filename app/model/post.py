from datetime import datetime
from app.model.comment import Comment

from app.model import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.SmallInteger, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship("User")

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    board = db.relationship("Board", back_populates="posts")

    comments = db.relationship('Comment', backref='post', lazy=True, primaryjoin='and_(Post.id == Comment.post_id, Comment.status != 2)')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Post title: %s, content: %s, description: %s, status: %d," \
               " created_at: %s, updated_at: %s>"\
               % (self.title, self.content, self.description, self.status,
                  self.created_at, self.updated_at)

    def set_user_id(self, uid):
        self.user_id = uid

    def set_board_id(self, bid):
        self.board_id = bid

    def set_title(self, title):
        self.title = title

    def set_content(self, content):
        self.content = content

    def set_description(self, description):
        self.description = description

    def set_updated_at(self):
        self.updated_at = datetime.utcnow()

    def change_status(self):
        self.status = 2


