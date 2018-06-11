from app.error import UserNotExistError
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
        # FIXME : user의 상태는 스스로
        user.status = UserStatus.INACTIVE
        db.session.flush()

    except Exception as e:
        db.session.rollback()
        raise e


def login(email, password):
    user = _get_user_by_email_and_password(email, password)

    if not user.is_active():
        raise UserNotExistError()

    return user


def _get_user_by_email_and_password(email, password):
    user = User.query.filter_by(email=email, password=password).one_or_none()
    return user


def is_exists(user):
    temp = User.query.filter(User.email == user.email).one_or_none()

    if temp:
        return True
    else:
        return False
