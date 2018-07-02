from app.error import NotFoundError, DuplicateValueError, WrongPasswordError
from app.model import db
from app.model.user import User


def register(user):
    if _is_duplicate_email(user.email):
        raise DuplicateValueError('이미 존재하는 이메일입니다.')

    try:
        user.set_password(user.password)

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    else:
        return user


def leave(user):
    try:
        # 상태는 객체 스스로 변경할 수 있다.
        user.leaved()
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e


def login(email, password):
    user = _get_user_by_email(email)
    if not user:
        raise NotFoundError('존재하지 않는 유저입니다.')
    if not user.check_password(password):
        raise WrongPasswordError('비밀번호가 일치하지 않습니다.')
    if not user.is_active():
        raise NotFoundError('탈퇴한 유저입니다.')

    return user


def _get_user_by_email(email):
    user = User.query.filter_by(email=email).one_or_none()
    return user


def _is_duplicate_email(email):
    temp = User.query.filter_by(email=email).one_or_none()
    return temp
