import enum

from sqlalchemy_utils import ChoiceType

from app.model import db
from flask_login import UserMixin

from app.model.likes import Likes
from werkzeug.security import generate_password_hash, check_password_hash

from app.model.timestamp import TimestampMixin


class UserStatus(enum.Enum):
    ACTIVE = 0
    INACTIVE = 2


class User(UserMixin, db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)

    status = db.Column(ChoiceType(UserStatus, impl=db.Integer()), default=UserStatus.ACTIVE)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return self.status == UserStatus.ACTIVE

    def leave(self):
        self.status = UserStatus.INACTIVE

    def is_exists(self):
        temp = User.query.filter(User.email == self.email).one_or_none()
        if temp:
            return True
        else:
            return False

    def is_liked(self, post_id):
        if Likes.query.filter(Likes.post_id == post_id, Likes.user_id == self.id).one_or_none():
            return True
        return False

    def __repr__(self):
        return "<User email: %s, password: %s, created_at: %s, updated_at: %s>" \
               % (self.email, self.password, self.created_at, self.updated_at)

