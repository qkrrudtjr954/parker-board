from datetime import datetime
from parker_board.model.comment import Comment
from parker_board.model import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.SmallInteger, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Post id: %d, title: %s, content: %s, description: %s, status: %d, user_id: %d," \
               " created_at: %s, updated_at: %s>"\
               % (self.id, self.title, self.content, self.description, self.status, self.user_id,
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


