from flask import Blueprint, jsonify, session
from parker_board.service import user_service
from webargs.flaskparser import use_args
from parker_board.schema.user import user_schema

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('', methods=['POST'])
@use_args(user_schema)
def register(user_args):
    result = user_service.register(user_args)

    return jsonify(result['message']), result['status_code']


@bp.route('/login', methods=['POST'])
@use_args(user_schema)
def login(user_args):
    result = user_service.login(user_args)

    return jsonify(result['message']), result['status_code']


@bp.route('/logout', methods=['POST'])
def logout():
    result = {'message':'No user who signed in.', 'status_code':400}

    if session.get('current_user', None):
        user = session.pop('current_user')
        result['message'] = user_schema.dump(user).data
        result['status_code'] = 200

    return jsonify(result['message']), result['status_code']



@bp.errorhandler(422)
def handle_unprocessable_entity(err):
    exc = getattr(err, 'exc')

    if exc:
        messages = exc.messages
    else:
        messages = ['Invalid request']

    return jsonify({
        'errors': messages
    }), 422
