from app.error import NotFoundError, DuplicateValueError
from app.model import db
from app.model.user import User


def register(user):
    if is_duplicate_email(user.email):
        raise DuplicateValueError('That Email already exists.')

    try:
        db.session.add(user)
        db.session.flush()

        return user

    except Exception as e:
        db.session.rollback()
        raise e


def leave(user):
    try:
        # 상태는 객체 스스로 변경할 수 있다.
        user.leaved()
        db.session.flush()

    except Exception as e:
        db.session.rollback()
        raise e


def login(email, password):
    user = _get_user_by_email_and_password(email, password)

    if not user:
        raise NotFoundError('No User.')

    if not user.is_active():
        raise NotFoundError('Leaved User.')

    return user


def _get_user_by_email_and_password(email, password):
    user = User.query.filter_by(email=email, password=password).one_or_none()
    return user


def is_duplicate_email(email):
    temp = User.query.filter_by(email=email).one_or_none()
    return temp
