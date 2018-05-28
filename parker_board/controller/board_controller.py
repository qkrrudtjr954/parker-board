from flask import Blueprint, request, jsonify
from parker_board.service import board_service
from parker_board.model.board import Board
from parker_board.schema.board import boards_schema, board_schema, patch_board_schema
from webargs.flaskparser import use_args, parser


bp = Blueprint('board', __name__)

'''
Board
목록, 생성, 삭제, 수정, 읽기
'''


# create board
@bp.route('/boards', methods=['POST'])
@use_args(board_schema)
def create(board_args):
    result = board_service.create(board_args)
    return jsonify(result['message']), result['status_code']


# read board
@bp.route('/boards/<int:bid>', methods=['GET'])
def read(bid):
    board = board_service.get(bid)
    return board_schema.jsonify(board), 200


# update board
# @bp.route('/boards/<int:bid>', methods=['PATCH'])
# def update(bid):
#     data = parser.parse(patch_board_schema)
#     result = board_service.update_board(bid, data)
#     return jsonify(result['message']), result['status_code']


# delete board
@bp.route('/boards/<int:bid>', methods=['DELETE'])
def delete(bid):
    result = board_service.delete(bid)
    return jsonify(result['message']), result['status_code']


# list board
@bp.route('/boards', methods=['GET'])
def list():
    boards = board_service.list()
    return boards_schema.jsonify(boards), 200


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
