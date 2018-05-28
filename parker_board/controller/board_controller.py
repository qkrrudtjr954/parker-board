from flask import Blueprint, request, jsonify
from parker_board.service import board_service
from parker_board.schema.board import boards_schema, BoardSchema
from webargs.flaskparser import use_args


bp = Blueprint('board', __name__)


@bp.route('/boards', methods=['POST'])
@use_args(BoardSchema())
def add_board(board_args):
    result = board_service.add_board(board_args)
    return jsonify(result['message']), result['status_code']



