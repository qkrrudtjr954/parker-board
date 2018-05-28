from flask import Blueprint, jsonify, session
from parker_board.service import user_service
from webargs.flaskparser import use_args
from parker_board.schema.login_schema import login_req_schema
from parker_board.schema.user import user_schema

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('', methods=['POST'])
@use_args(login_req_schema)
def register(args):
    '''
    회원 가입 가능
    가입 실패시 롤백 가능
    :param args: email, password
    :return: json message and status code.
    '''
    new_user = user_schema.load(args).data

    result = user_service.register_user(new_user)

    return jsonify(result['message']), result['status_code']


@bp.route('/login', methods=['POST'])
@use_args(login_req_schema)
def login(args):
    '''
    로그인 가능
    세션에 유저정보 저장 가능
    :param args: email, password
    :return: json message and status code.
    '''
    user = user_schema.load(args).data

    result = user_service.login_user(user)

    return jsonify(result['message']), result['status_code']


@bp.route('/logout', methods=['POST'])
def logout():
    '''
    현재 세션에 있는 current_user를 삭제한다.
    :return: json message and status code.
    '''
    result = {'message':'No user who signed in.', 'status_code':400}

    if session.get('current_user', None) is not None:
        user = session.pop('current_user')
        result['message'] = '{} logged out.'.format(user)
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
