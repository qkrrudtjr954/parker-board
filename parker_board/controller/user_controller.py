from flask import Blueprint, jsonify, session
from parker_board import login_manager
from parker_board.model.user import User
from parker_board.service import user_service
from webargs.flaskparser import use_args
from parker_board.schema.user import user_schema
from parker_board.schema.resp import resp_schema
from flask_login import login_user, login_required, logout_user

bp = Blueprint('user', __name__, url_prefix='/users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route('/login', methods=['POST'])
@use_args(user_schema)
def login(user_args):
    result = user_service.get_user_by_email_and_password(user_args)

    if result['status']:
        login_user(user_schema.load(result['data']).data)
        result['status_code'] = 200
    else:
        result['status_code'] = 400

    return resp_schema.jsonify(result), result['status_code']


@bp.route('/logout')
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



@bp.errorhandler(422)
def handle_unprocessable_entity(err):
    exc = getattr(err, 'exc')

    if exc:
        messages = exc.messages
    else:
        messages = ['Invalid request']

    return jsonify({
        'data': messages, 'status_code' : 422
    }), 422

