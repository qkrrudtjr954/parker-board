from parker_board.model import db
from parker_board.model.board import Board
from parker_board.model.post import Post
from parker_board.model.comment import Comment
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    status = db.Column(db.SmallInteger, default=0)

    boards = db.relationship('Board', backref='user', lazy=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User email: %s, password: %s, created_at: %s, updated_at: %s>" \
               % (self.email, self.password, self.created_at, self.updated_at)


    def leave(self):
        self.status = 2