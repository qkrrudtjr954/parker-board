from flask import Blueprint
from parker_board.service import board_service
from parker_board.schema.board import board_schema
from webargs.flaskparser import use_args
from flask_login import login_required, current_user
from parker_board.schema.resp import resp_schema


bp = Blueprint('board', __name__)

'''
Board
목록, 생성, 삭제, 수정
'''


# create board
@bp.route('/boards', methods=['POST'])
@use_args(board_schema)
@login_required
def create(board_args):
    board_args.set_user_id(current_user.id)
    result = board_service.create(board_args)
    print(result)
    return resp_schema.jsonify(result), result['status_code']


# update board
@bp.route('/boards/<int:bid>', methods=['PATCH'])
@use_args(board_schema)
@login_required
def update(board_args, bid):
    result = board_service.update(bid, board_args)
    return resp_schema.jsonify(result), result['status_code']


# delete board
@bp.route('/boards/<int:bid>', methods=['DELETE'])
@login_required
def delete(bid):
    result = board_service.delete(bid)
    return resp_schema.jsonify(result), result['status_code']
