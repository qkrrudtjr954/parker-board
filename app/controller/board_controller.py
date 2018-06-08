from flask import Blueprint, request, jsonify

from app.model.board import Board
from app.service import board_service
from app.schema.board import board_schema, main_board_schema, after_fix_board_schema, after_del_board_schema
from webargs.flaskparser import use_args
from flask_login import login_required, current_user
from app.schema.pagination import pagination_schema


bp = Blueprint('board', __name__)

'''
Board
목록, 생성, 삭제, 수정
'''


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
@use_args(board_schema)
def create(board: Board):
    try:
        board_service.create(board, current_user)
        return after_fix_board_schema.jsonify(board), 200
    except Exception:
        return 'Server Error.', 500


# update board
@bp.route('/boards/<int:board_id>', methods=['PATCH'])
@use_args(board_schema)
@login_required
def update(board_data, board_id):
    target_board = board_service.get_board(board_id)

    if target_board:
        if target_board.user_id == current_user.id:
            try:
                board_service.update(target_board, board_data)
                return after_fix_board_schema.jsonify(target_board), 200

            except Exception:
                return 'Server Error.', 500
        else:
            return 'No Authentication.', 401
    else:
        return 'No Board.', 400


# delete board
@bp.route('/boards/<int:board_id>', methods=['DELETE'])
@login_required
def delete(board_id):
    target_board = board_service.get_board(board_id)

    if target_board:
        if target_board.user_id == current_user.id:
            try:
                board_service.delete(target_board)
                return after_del_board_schema.jsonify(target_board), 200
            except Exception:
                return 'Server Error.', 500
        else:
            return 'No Authentication.', 401
    else:
        return 'No Board', 400

