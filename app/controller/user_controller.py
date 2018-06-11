from flask import Blueprint, request, jsonify
from app import login_manager
from app.error import UserNotExistError
from app.model.user import User
from app.service import user_service
from webargs.flaskparser import use_args
from app.schema.user import user_schema, after_register_schema, after_leave_schema, after_login_schema
from flask_login import login_user, login_required, logout_user, current_user


bp = Blueprint('user', __name__, url_prefix='/users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/login', methods=['POST'])
@use_args(user_schema)
def login(user):
    next = request.args.get('next') if 'next' in request.args else '/'

    try:
        logged_in_user = user_service.login(user.email, user.password)

        if logged_in_user:
            login_user(logged_in_user)
            return jsonify(dict(user=after_login_schema.dump(logged_in_user).data, next=next)), 200
        else:
            return 'No User.', 400

    except UserNotExistError as e:
        return 'Leaved User.', 400



@bp.route('/logout', methods=['DELETE'])
@login_required
def logout():
    logout_user()
    return 'Log out', 200


@bp.route('/', methods=['POST'])
@use_args(user_schema)
def register(user):
    if not user_service.is_exists(user):
        try:
            user_service.register(user)
        except Exception:
            return 'Server Error.', 500
        else:
            return after_register_schema.jsonify(user), 200
    else:
        return 'That Email already exists.', 400


@bp.route('/', methods=['DELETE'])
@login_required
def leave():
    try:
        user_service.leave(current_user)
    except Exception:
        return 'Server Error.', 500
    else:
        return after_leave_schema.jsonify(current_user), 200

