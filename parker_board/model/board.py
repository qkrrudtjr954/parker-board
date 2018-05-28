from datetime import datetime
from parker_board.model import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.SmallInteger, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # posts = db.relationship('Post', backref='board', lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Board id: %d, title: %s, description: %s, status: %d," \
               " created_at: %s, updated_at: %s>"\
               % (self.id, self.title, self.description, self.status,
                  self.created_at, self.updated_at)
