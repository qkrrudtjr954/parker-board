import datetime

from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

from app import User
from app.error import NotFoundError, DuplicateValueError, WrongPasswordError
from app.service import user_service
from app.schema.user import after_register_schema, after_login_schema, before_login_schema, before_register_schema, \
    user_info_schema, is_logged_in_schema
from app.schema.error import default_message_error_schema

from webargs.flaskparser import use_args

login_manager = LoginManager()

bp = Blueprint('user', __name__, url_prefix='/users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    next = request.path if request.path else '/'

    result = dict(message='Login First.', next=next)
    return default_message_error_schema.jsonify(result), 401


@bp.route('/login', methods=['POST'])
@use_args(before_login_schema)
def login(login_data):
    next = request.args.get('next') if 'next' in request.args else '/'

    try:
        # 로그인한 유저를 반환한다. -> login 의 기능에만 충실하는 코드
        logged_in_user = user_service.login(login_data.email, login_data.password)
        login_user(logged_in_user, remember=True, duration=datetime.timedelta(hours=1))

        return jsonify(dict(user=after_login_schema.dump(logged_in_user).data, next=next)), 200

    except WrongPasswordError as e1:
        error = dict(message=e1.message)
        return default_message_error_schema.jsonify(error), 400

    except NotFoundError as e:
        error = dict(message=e.message)
        return default_message_error_schema.jsonify(error), 400


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return 'Log out', 200


@bp.route('/', methods=['POST'])
@use_args(before_register_schema)
def register(register_data):
    try:
        register_user = user_service.register(register_data)

    except DuplicateValueError as e:
        return default_message_error_schema.jsonify(dict(message=e.message)), 400

    except Exception:
        return default_message_error_schema.jsonify(dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')), 500

    else:
        return after_register_schema.jsonify(register_user), 200


@bp.route('/leave', methods=['PATCH'])
@login_required
def leave():
    try:
        user_service.leave(current_user)
    except Exception:
        return default_message_error_schema.jsonify(dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')), 500
    else:
        logout_user()
        return 'leave', 204


@bp.route('/user-info', methods=['GET'])
@login_required
def get_current_user_info():
    return user_info_schema.jsonify(current_user), 200


@bp.route('/is-logged-in')
def is_logged_in():
    result = dict(is_logged_in=current_user.is_authenticated)
    return is_logged_in_schema.jsonify(result), 200

