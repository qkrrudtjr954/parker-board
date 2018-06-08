import enum

from sqlalchemy_utils import ChoiceType

from app.model import db
from flask_login import UserMixin
from datetime import datetime
from flask_login import current_user


class UserStatus(enum.Enum):
    ACTIVES = 0
    INACTIVE = 2


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)

    status = db.Column(ChoiceType(UserStatus, impl=db.Integer()), default=UserStatus.ACTIVES)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User email: %s, password: %s, created_at: %s, updated_at: %s>" \
               % (self.email, self.password, self.created_at, self.updated_at)

