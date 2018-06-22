from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from webargs.flaskparser import use_args

from app.model.board import Board, BoardStatus
from app.service import board_service
from app.schema.board import main_board_schema, board_create_form_schema, board_update_form_schema, board_redirect_schema
from app.schema.pagination import pagination_schema


bp = Blueprint('board', __name__)


@bp.route('/boards', methods=['GET'])
def main():
    boards = Board.query.filter(Board.status != BoardStatus.DELETED).all()

    return main_board_schema.jsonify(boards), 200


# create board
@bp.route('/boards', methods=['POST'])
@login_required
@use_args(board_create_form_schema)
def create(board: Board):
    try:
        board_service.create(current_user, board)
        return board_redirect_schema.jsonify(board), 200
    except Exception as e:
        print(e)
        return 'Server Error.', 500


# update board
@bp.route('/boards/<int:board_id>', methods=['PATCH'])
@use_args(board_update_form_schema)
@login_required
def update(board_data, board_id):
    target_board = Board.query.get(board_id)

    if not target_board:
        return 'No Board.', 404

    if not target_board.user_id == current_user.id:
        return 'No Authentication.', 401

    try:
        board_service.update(target_board, board_data)
        return board_redirect_schema.jsonify(target_board), 200
    except Exception:
        return 'Server Error.', 500


# delete board
@bp.route('/boards/<int:board_id>', methods=['DELETE'])
@login_required
def delete(board_id):
    target_board = Board.query.get(board_id)

    if not target_board:
        return 'No Board.', 404

    if not target_board.user_id == current_user.id:
        return 'No Authentication.', 401

    try:
        board_service.delete(target_board)
        return board_redirect_schema.jsonify(target_board), 204
    except Exception as e:
        return 'Server Error.', 500
