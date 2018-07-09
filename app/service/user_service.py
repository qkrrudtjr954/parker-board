from app.error import NotFoundError, DuplicateValueError, WrongPasswordError
from app.model import db
from app.model.user import User


def register(user):
    if _get_user_by_email(user.email):
        raise DuplicateValueError('이미 존재하는 이메일입니다.')

    try:
        user.encode_password()

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    else:
        return user


def leave(user: User):
    try:
        # 상태는 객체 스스로 변경할 수 있다.
        user.leave()
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

