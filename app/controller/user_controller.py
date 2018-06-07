from flask import Blueprint, request
from app import login_manager
from app.model.user import User, UserStatus
from app.service import user_service
from webargs.flaskparser import use_args
from app.schema.user import user_schema, login_schema
from app.schema.resp import resp_schema
from flask_login import login_user, login_required, logout_user, current_user

bp = Blueprint('user', __name__, url_prefix='/users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/login', methods=['GET'])
def login_view():
    return str('login view.')


@bp.route('/login', methods=['POST'])
@use_args(login_schema)
def login_logic(user_args):
    result = {}
    next = request.args.get('next') if 'next' in request.args else '/'

    user = user_service.login(user_args)

    if user:
        if user.status == UserStatus.INACTIVE:
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
    result = dict(data='logout.', status_code=200)

    return resp_schema.jsonify(result), result['status_code']


@bp.route('', methods=['POST'])
@use_args(login_schema)
def register(user_args):
    result = user_service.register(user_args)
    return resp_schema.jsonify(result), result['status_code']


@bp.route('/<int:uid>', methods=['DELETE'])
@login_required
def leave(uid):
    if current_user.id == uid:
        result = user_service.leave(uid)
    else:
        result = dict(errors='Wrong Access.', status_code=400)

    return resp_schema.jsonify(result), result['status_code']
