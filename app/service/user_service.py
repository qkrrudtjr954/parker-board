from app.model import db

# user에 필요한 모든 로직을 service 로 옮기고 web 에 관련된 내용만 controller로 빼라.
def register(user):
    try:
        db.session.add(user)
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def leave(user):
    try:
        user.be_inactive()
        db.session.flush()
    except Exception:
        db.session.rollback()
        raise e
