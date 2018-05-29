from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from parker_board.schema.comment import comment_schema
from parker_board.service import comment_service


bp = Blueprint('comment', __name__)

'''
댓글 
생성, 삭제, 수정
'''


@bp.route('/posts/<int:pid>/comments', methods=['POST'])
@use_args(comment_schema)
def create(comment_args, pid):
    result = comment_service.create(comment_args, pid)

    return jsonify(result['message']), result['status_code']


@bp.route('/comments/<int:cid>', methods=['DELETE'])
def delete(cid):
    result = comment_service.delete(cid)

    return jsonify(result['message']), result['status_code']


# @bp.route('/comments/<int:cid>', methods=['PATCH'])
# def update(cid):
#     result = comment_service.update(cid)
#
#     return jsonify(result['message']), result['status_code']
