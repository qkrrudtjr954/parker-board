from flask import Blueprint, request
from app import login_manager
from app.model.user import User
from app.service import user_service
from webargs.flaskparser import use_args
from app.schema.user import user_schema, after_register_schema, after_leave_schema
from app.schema.resp import resp_schema
from flask_login import login_user, login_required, logout_user


bp = Blueprint('user', __name__, url_prefix='/users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/login', methods=['POST'])
@use_args(user_schema)
def login(user):
    result = {}
    next = request.args.get('next') if 'next' in request.args else '/'

    user = User.query.filter_by(email=user.email, password=user.password).one_or_none()

    if user:
        if user.is_inactive():
            result['errors'] = dict(message='Leaved User.')
            result['status_code'] = 401
        else:
            login_user(user)

            result['data'] = dict(user=user_schema.dump(user).data, next=next)
            result['status_code'] = 200
    else:
        result['errors'] = dict(message='No User.')
        result['status_code'] = 400

    return resp_schema.jsonify(result), result['status_code']


@bp.route('/logout', methods=['DELETE'])
@login_required
def logout():
    logout_user()
    return resp_schema.jsonify(dict(data='logout')), 200


@bp.route('', methods=['POST'])
@use_args(user_schema)
def register(user):
    result = {}

    if not user.is_exists():
        try:
            user_service.register(user)
        except Exception:
            result['errors'] = dict(message='Server Error.')
            result['status_code'] = 500
        else:
            result['data'] = after_register_schema.dump(user).data
            result['status_code'] = 200
    else:
        result['errors'] = dict(message='That Email already exists.')
        result['status_code'] = 400

    return resp_schema.jsonify(result), result['status_code']


@bp.route('/<int:uid>', methods=['DELETE'])
@login_required
def leave(uid):
    # current_user 를 leave 시키면 됨.
    result = {}

    user = User.query.get(uid)

    if user:
        if user.is_current_user():
            try:
                user_service.leave(user)
            except Exception:
                result['errors'] = dict(message='Server Error. Please try again.')
                result['status_code'] = 500
            else:
                result['data'] = after_leave_schema.dump(user).data
                result['status_code'] = 200
        else:
            result = dict(errors='Wrong Access.', status_code=400)
    else:
        result = dict(errors='No User.', status_code=401)

    return resp_schema.jsonify(result), result['status_code']

