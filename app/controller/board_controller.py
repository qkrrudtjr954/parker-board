from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from webargs.flaskparser import use_args

from app.model.board import Board
from app.schema.error import default_message_error_schema
from app.service import board_service
from app.schema.board import main_board_schema, board_create_form_schema, board_update_form_schema, board_id_schema, \
    simple_board_schema, concrete_board_schema

bp = Blueprint('board', __name__)


@bp.route('/boards', methods=['GET'])
def main():
    boards = Board.query.filter(~Board.is_deleted).all()
    return main_board_schema.jsonify(boards), 200


@bp.route('/boards/<int:board_id>', methods=['GET'])
def get_board(board_id):
    target_board = Board.query.get(board_id)

    if not target_board:
        error = dict(message='존재하지 않는 게시판 입니다.')
        return default_message_error_schema.jsonify(error), 404

    return concrete_board_schema.jsonify(target_board), 200


# create board
@bp.route('/boards', methods=['POST'])
@login_required
@use_args(board_create_form_schema)
def create(board: Board):
    try:
        board_service.create(current_user, board)
        return board_id_schema.jsonify(board), 200
    except Exception:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500


# update board
@bp.route('/boards/<int:board_id>', methods=['PATCH'])
@use_args(board_update_form_schema)
@login_required
def update(board_data, board_id):
    target_board = Board.query.get(board_id)

    if not target_board:
        error = dict(message='존재하지 않는 게시판 입니다.')
        return default_message_error_schema.jsonify(error), 404

    if not target_board.is_owner(current_user):
        error = dict(message='권한이 없습니다.')
        return default_message_error_schema.jsonify(error), 401

    try:
        board_service.update(target_board, board_data)
        return board_id_schema.jsonify(target_board), 200
    except Exception:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500


# delete board
@bp.route('/boards/<int:board_id>', methods=['DELETE'])
@login_required
def delete(board_id):
    target_board = Board.query.get(board_id)

    if not target_board:
        error = dict(message='존재하지 않는 게시판 입니다.')
        return default_message_error_schema.jsonify(error), 404

    if not target_board.is_owner(current_user):
        error = dict(message='권한이 없습니다.')
        return default_message_error_schema.jsonify(error), 401

    try:
        board_service.delete(target_board)
        return board_id_schema.jsonify(target_board), 204
    except Exception as e:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500

