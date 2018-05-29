from flask import session
from parker_board.model import db
from parker_board.model.user import User
from parker_board.schema.user import user_schema


def register(new_user):
    result = {}

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        result['status_code'] = 400
        result['message'] = 'Duplicate Email.'
        db.session.rollback()
    else:
        result['status_code'] = 200
        result['message'] = 'User registerd.'

    return result


def login(user):
    result = {}
    temp_user = User.query.filter_by(email=user.email).filter_by(password=user.password).one_or_none()

    if temp_user is None:
        result['status_code'] = 400
        result['message'] = 'No User.'
    elif temp_user.status == 2:
        result['status_code'] = 400
        result['message'] = 'Leave User.'
    else:
        session['current_user'] = user_schema.dump(temp_user).data

        result['status_code'] = 200
        result['message'] = user_schema.dump(temp_user).data

    return result


def leave(uid):
    result = {}

    user = User.query.get(uid)
    current_user = user_schema.load(session.get('current_user')).data

    if user == current_user:
        user.leave()

        db.session.add(user)
        db.session.commit()

        result['status_code'] = 200
        result['message'] = 'User Leave.'
    else:
        result['status_code'] = 400
        result['message'] = 'Bad Request'

    return result

