from app.model import db
from app.model.user import User, UserStatus


def register(user):
    try:
        db.session.add(user)
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def leave(user):
    try:
        user.status = UserStatus.INACTIVE.value
        db.session.flush()

    except Exception as e:
        db.session.rollback()
        raise e


def get_user_by_email_and_password(email, password):
    user = User.query.filter_by(email=email, password=password).one_or_none()
    return user


def is_exists(user):
    temp = User.query.filter(User.email == user.email).one_or_none()

    if temp:
        return True
    else:
        return False


def is_active(user):
    if user.status == UserStatus.INACTIVE:
        return False
    else:
        return True
