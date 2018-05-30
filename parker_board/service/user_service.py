from parker_board.model import db
from parker_board.model.user import User
from parker_board.schema.user import user_schema
from sqlalchemy.exc import IntegrityError


def register(new_user):
    result = {}

    try:
        db.session.add(new_user)
        db.session.commit()
        result['data'] = user_schema.dump(new_user).data
        result['status'] = True

    except IntegrityError:
        db.session.rollback()

        result['data'] = 'Duplicate Email'
        result['status'] = False

    except Exception:
        db.session.rollback()
        result['data'] = 'Server Error. Please try again.'
        result['status'] = False

    return result


def get_user_by_email_and_password(user_data):
    user = User.query.filter_by(email=user_data.email, password=user_data.password).first()

    result = {}

    if user:
        result['data'] = user_schema.dump(user).data
        result['status'] = True
    else:
        result['data'] = 'No User.'
        result['status'] = False

    return result

