from flask import Blueprint, request, jsonify
from app import login_manager
from app.error import NotFoundError, DuplicateValueError
from app.model.user import User
from app.service import user_service
from webargs.flaskparser import use_args
from app.schema.user import after_register_schema, after_leave_schema, after_login_schema, \
    before_login_schema, before_register_schema
from flask_login import login_user, login_required, logout_user, current_user


bp = Blueprint('user', __name__, url_prefix='/users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/login', methods=['POST'])
@use_args(before_login_schema)
def login(login_data):

    next = request.args.get('next') if 'next' in request.args else '/'

    try:
        # 로그인한 유저를 반환한다. -> login 의 기능에만 충실하는 코드
        logged_in_user = user_service.login(login_data.email, login_data.password)
        testing = login_user(logged_in_user, remember=True)

        return jsonify(dict(user=after_login_schema.dump(logged_in_user).data, next=next)), 200

    except NotFoundError as e:
        return e.message, 400


@bp.route('/logout', methods=['DELETE'])
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
        return e.message, 400

    except Exception:
        return 'Server Error.', 500

    else:
        return after_register_schema.jsonify(register_user), 200


@bp.route('/', methods=['DELETE'])
@login_required
def leave():
    try:
        user_service.leave(current_user)
    except Exception:
        return 'Server Error.', 500
    else:
        return after_leave_schema.jsonify(current_user), 200

