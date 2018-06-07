from flask import Blueprint
from webargs.flaskparser import use_args
from app.schema.comment import comment_schema
from app.service import comment_service
from app.schema.resp import resp_schema


bp = Blueprint('comment', __name__)

'''
댓글 
생성, 삭제, 수정
'''


@bp.route('/posts/<int:pid>/comments', methods=['POST'])
@use_args(comment_schema)
def create(comment_args, pid):
    result = comment_service.create(comment_args, pid)

    return resp_schema.jsonify(result), result['status_code']


@bp.route('/comments/<int:cid>', methods=['DELETE'])
def delete(cid):
    result = comment_service.delete(cid)

    return resp_schema.jsonify(result), result['status_code']


@bp.route('/comments/<int:cid>', methods=['PATCH'])
@use_args(comment_schema)
def update(comment_args, cid):
    result = comment_service.update(cid, comment_args)

    return resp_schema.jsonify(result), result['status_code']