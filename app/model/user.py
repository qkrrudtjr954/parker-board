import enum

from sqlalchemy_utils import ChoiceType

from app.model import db
from flask_login import UserMixin
from datetime import datetime

from app.model.like import Like


class UserStatus(enum.Enum):
    ACTIVE = 0
    INACTIVE = 2


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)

    status = db.Column(ChoiceType(UserStatus, impl=db.Integer()), default=UserStatus.ACTIVE)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_active(self):
        return self.status == UserStatus.ACTIVE

    def leaved(self):
        self.status = UserStatus.INACTIVE

    def is_exists(self):
        temp = User.query.filter(User.email == self.email).one_or_none()
        if temp:
            return True
        else:
            return False

    def is_liked(self, post_id):
        if Like.query.filter(Like.post_id == post_id, Like.user_id == self.id).one_or_none():
            return True
        return False

    def __repr__(self):
        return "<User email: %s, password: %s, created_at: %s, updated_at: %s>" \
               % (self.email, self.password, self.created_at, self.updated_at)

