from flask import Blueprint, jsonify, redirect, abort
from parker_board.service import board_service
from parker_board.schema.board import board_schema
from webargs.flaskparser import use_args
from flask_login import login_required, current_user
from parker_board.schema.resp import resp_schema
from parker_board.model.board import Board


bp = Blueprint('board', __name__)

'''
Board
목록, 생성, 삭제, 수정, 읽기
'''

@bp.route('/boards/create', methods=['GET'])
@login_required
def board_create_view():
    return 'board view'


# create board
@bp.route('/boards', methods=['POST'])
@use_args(board_schema)
@login_required
def create(board_args):
    result = {}

    board_args.set_user_id(current_user.id)

    if board_service.create(board_args):
        # result['data'] = dict(board=board_schema.dump(board_args).data)
        # result['status_code'] = 200
        return redirect('/boards/%d/posts' % board_args.id)
    else:
        return resp_schema.jsonify(
            dict(errors=dict(error='Server Error. Please Try again.'), status_code=500)
        ), 500


@bp.route('/boards/<int:uid>/update', methods=['GET'])
@login_required
def board_update_view(uid):
    board = Board.query.get(uid)

    if board:
        return board_schema.jsonify(board), 200
    else:
        abort(404, 'No Board.')


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
    return jsonify(result['message']), result['status_code']
