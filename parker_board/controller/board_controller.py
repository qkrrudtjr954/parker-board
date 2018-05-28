from flask import Blueprint, request, jsonify
from parker_board.service import board_service
from parker_board.model.board import Board
from parker_board.schema.board import boards_schema, board_schema, patch_board_schema
from webargs.flaskparser import use_args, parser


bp = Blueprint('board', __name__)


@bp.route('/boards', methods=['POST'])
@use_args(board_schema)
def add_board(board_args):
    result = board_service.add_board(board_args)
    return jsonify(result['message']), result['status_code']


@bp.route('/boards', methods=['GET'])
def get_all_board():
    boards = Board.query.all()
    return boards_schema.jsonify(boards), 200


@bp.route('/boards/<int:board_id>', methods=['GET'])
def get_board(board_id):
    board = Board.query.get(board_id)
    return board_schema.jsonify(board), 200


@bp.route('/boards/<int:board_id>', methods=['DELETE'])
def remove_board(board_id):
    result = board_service.remove_board(board_id)
    return jsonify(result['message']), result['status_code']


# @bp.route('/boards/<int:board_id>', methods=['PATCH'])
# def update_board(board_id):
#     data = parser.parse(patch_board_schema)
#     result = board_service.update_board(board_id, data)
#     return jsonify(result['message']), result['status_code']



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
