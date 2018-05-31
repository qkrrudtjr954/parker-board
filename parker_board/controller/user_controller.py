from flask import Blueprint, request, redirect
from parker_board import login_manager
from parker_board.model.user import User
from parker_board.service import user_service
from webargs.flaskparser import use_args
from parker_board.schema.user import user_schema
from parker_board.schema.resp import resp_schema
from flask_login import login_user, login_required, logout_user, current_user

bp = Blueprint('user', __name__, url_prefix='/users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/login', methods=['GET'])
def login_view():
    return str('login view.')


@bp.route('/login', methods=['POST'])
@use_args(user_schema)
def login_logic(user_args):
    result = {}

    next = request.args.get('next') if 'next' in request.args else '/'

    user = User.query.filter_by(email=user_args.email, password=user_args.password).first()

    if user:
        login_user(user)

        result['data'] = dict(user=user_schema.dump(user).data, next=next)
        result['status_code'] = 200
    else:
        result['errors'] = dict(error='No User.')
        result['status_code'] = 401

    return resp_schema.jsonify(result), result['status_code']




















@bp.route('/logout', methods=['DELETE'])
@login_required
def logout():
    logout_user()
    result = dict(data='logout.', status_code=200)

    return resp_schema.jsonify(result), result['status_code']


@bp.route('', methods=['POST'])
@use_args(user_schema)
def register(user_args):
    result = user_service.register(user_args)

    if result['status']:
        result['status_code'] = 200
    else:
        result['status_code'] = 400

    return resp_schema.jsonify(result), result['status_code']


@bp.route('/<int:uid>', methods=['DELETE'])
@login_required
def leave(uid):
    if current_user.id == uid:
        result = user_service.leave(uid)

        if result['status']:
            result['status_code'] = 200
        else:
            result['status_code'] = 500
    else:
        result = dict(errors='Wrong Access.', status_code=400)

    return resp_schema.jsonify(result), result['status_code']
