from flask import Blueprint, jsonify
from parker_board.service import board_service
from parker_board.schema.board import board_schema
from webargs.flaskparser import use_args
from flask_login import login_required


bp = Blueprint('board', __name__)

'''
Board
목록, 생성, 삭제, 수정, 읽기
'''


# create board
@bp.route('/boards', methods=['POST'])
@use_args(board_schema)
@login_required
def create(board_args):
    result = board_service.create(board_args)
    return jsonify(result['message']), result['status_code']


# read board
@bp.route('/boards/<int:bid>', methods=['GET'])
@login_required
def read(bid):
    result = board_service.get(bid)
    return jsonify(result['message']), result['status_code']


# update board
@bp.route('/boards/<int:bid>', methods=['PATCH'])
@use_args(board_schema)
@login_required
def update(board_args, bid):
    result = board_service.update(bid, board_args)
    return jsonify(result['message']), result['status_code']


# delete board
@bp.route('/boards/<int:bid>', methods=['DELETE'])
@login_required
def delete(bid):
    result = board_service.delete(bid)
    return jsonify(result['message']), result['status_code']


# list board
@bp.route('/boards', methods=['GET'])
def list():
    result = board_service.list()
    return jsonify(result['message']), result['status_code']


@bp.errorhandler(422)
def board_validation_handler(err):
    exc = getattr(err, 'exc')

    if exc:
        messages = exc.messages
    else:
        messages = ['Invalid request']

    return jsonify({
        'errors': messages
    }), 422
