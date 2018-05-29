from flask import Blueprint, jsonify
from webargs.flaskparser import use_args, parser
from parker_board.service import board_service, post_service
from parker_board.schema.post import posts_schema, post_schema


bp = Blueprint('post', __name__)


'''
글
목록, 생성, 삭제, 수정, 읽기
'''


# list post
# GET /boards/1/posts
@bp.route('/boards/<int:bid>/posts', methods=['GET'])
def list(bid):
    result = post_service.list(bid)

    return jsonify(result['message']), result['status_code']


# create post
# POST /boards/1/posts
@bp.route('/boards/<int:bid>/posts', methods=['POST'])
@use_args(post_schema)
def create(post_args, bid):
    result = post_service.create(bid, post_args)

    return jsonify(result['message']), result['status_code']


# read post
# GET /posts/1
@bp.route('/posts/<int:pid>')
def read(pid):
    result = post_service.get(pid)

    return jsonify(result['message']), result['status_code']


# # update post
# # PATCH /posts/1
# @bp.route('/posts/<int:pid>', methods=['PATCH'])
# def update(pid):


# delete post
# DELETE /posts/1
@bp.route('/posts/<int:pid>', methods=['DELETE'])
def delete(pid):
    result = post_service.delete(pid)

    return jsonify(result['message']), result['status_code']


@bp.errorhandler(422)
def post_validation_handler(err):
    exc = getattr(err, 'exc')

    if exc:
        messages = exc.messages
    else:
        messages = ['Invalid request']

    return jsonify({
        'errors': messages
    }), 422



