from flask import Blueprint, request, jsonify

from app.model.board import Board
from app.service import board_service
from app.schema.board import main_board_schema, after_fix_board_schema, after_del_board_schema, before_create_board_schema, before_update_board_schema
from webargs.flaskparser import use_args
from flask_login import login_required, current_user
from app.schema.pagination import pagination_schema


bp = Blueprint('board', __name__)


@bp.route('/boards/', methods=['GET'])
@use_args(pagination_schema)
def main(pagination):
    boards = board_service.pagination_boards(pagination.page, pagination.per_page)

    boards_items = main_board_schema.dump(boards.items).data
    pagination = pagination_schema.dump(boards).data

    result = dict(boards=boards_items, pagenation=pagination)

    return jsonify(result), 200


# create board
@bp.route('/boards', methods=['POST'])
@login_required
@use_args(before_create_board_schema)
def create(board: Board):
    try:
        board_service.create(current_user, board)
        return after_fix_board_schema.jsonify(board), 200
    except Exception:
        return 'Server Error.', 500


# update board
@bp.route('/boards/<int:board_id>', methods=['PATCH'])
@use_args(before_update_board_schema)
@login_required
def update(board_data, board_id):
    target_board = Board.query.get(board_id)

    if not target_board:
        return 'No Board.', 400

    if not target_board.user_id == current_user.id:
        return 'No Authentication.', 401

    try:
        board_service.update(target_board, board_data)
        return after_fix_board_schema.jsonify(target_board), 200
    except Exception:
        return 'Server Error.', 500


# delete board
@bp.route('/boards/<int:board_id>', methods=['DELETE'])
@login_required
def delete(board_id):
    target_board = Board.query.get(board_id)

    if not target_board:
        return 'No Board.', 400

    if not target_board.user_id == current_user.id:
        return 'No Authentication.', 401

    try:
        board_service.delete(target_board)
        return after_del_board_schema.jsonify(target_board), 200
    except Exception:
        return 'Server Error.', 500
