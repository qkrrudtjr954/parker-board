from flask import Blueprint, jsonify
from webargs.flaskparser import use_args, parser
from parker_board.service import board_service, post_service
from parker_board.schema.post import posts_schema, post_schema


bp = Blueprint('post', __name__, url_prefix='/boards/<int:bid>')


@bp.route('/posts', methods=['GET'])
def get_all_post(bid):
    board = board_service.get_board(bid)

    posts = board.posts

    return posts_schema.jsonify(posts), 200


@bp.route('/posts', methods=['POST'])
@use_args(post_schema)
def add_post(post_args, bid):
    board = board_service.get_board(bid)

    result = post_service.add_post(board, post_args)

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



