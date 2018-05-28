from flask import Blueprint, jsonify
from webargs.flaskparser import use_args, parser
from parker_board.service import board_service, post_service
from parker_board.schema.post import posts_schema, post_schema


bp = Blueprint('post', __name__, url_prefix='/boards/<int:bid>')


'''
글
목록, 생성, 삭제, 수정, 읽기
'''


# list post
@bp.route('/posts', methods=['GET'])
def list(bid):
    board = board_service.get(bid)

    posts = board.posts

    return posts_schema.jsonify(posts), 200


# create post
@bp.route('/posts', methods=['POST'])
@use_args(post_schema)
def create(post_args, bid):
    board = board_service.get(bid)

    result = post_service.create(board, post_args)

    return jsonify(result['message']), result['status_code']


# delete post
@bp.route('/posts/<int:pid>')
def delete(bid, pid):
    board = board_service.get(bid)

    result = post_service.delete(pid)


# update post

# read post
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



