from app.model import db
from app.model.user import User
from app.schema.user import user_schema
from sqlalchemy.exc import IntegrityError


def register(user_data):
    result = {}

    try:
        new_user = user_schema.load(user_data).data

        db.session.add(new_user)
        db.session.flush()
        result['data'] = user_schema.dump(new_user).data
        result['status_code'] = 200

    except IntegrityError:
        db.session.rollback()

        result['errors'] = dict(message='Duplicate Email.')
        result['status_code'] = 400

    except Exception as e:
        print(e)
        db.session.rollback()
        result['errors'] = dict(message='Server Error. Please try again.')
        result['status_code'] = 500

    return result


def login(user_data):
    user = User.query.filter_by(email=user_data['email'], password=user_data['password']).first()
    return user


def leave(uid):
    user = User.query.get(uid)
    result = {}

    if user:
        user.status = 2

        try:
            db.session.add(user)
            db.session.flush()

            result['data'] = dict(user=user_schema.dump(user).data)
            result['status_code'] = 200
        except Exception:
            db.session.rollback()
            result['errors'] = dict(message='Server Error. Please try again.')
            result['status_code'] = 500

        return result
    else:
        result['errors'] = dict(message='No User')
        result['status_code'] = 500