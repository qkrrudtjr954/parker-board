from flask import Blueprint, jsonify, abort, redirect
from webargs.flaskparser import use_args
from parker_board.service import post_service
from parker_board.model.board import Board
from parker_board.model.post import Post
from parker_board.schema.post import posts_schema, post_schema
from parker_board.schema.board import board_schema
from parker_board.schema.resp import resp_schema
from flask_login import login_required, current_user



bp = Blueprint('post', __name__)


'''
글
목록, 생성, 삭제, 수정, 읽기
'''


# list post
# GET /boards/1/posts
@bp.route('/boards/<int:bid>/posts', methods=['GET'])
@login_required
def post_view(bid):
    board = Board.query.get(bid)

    if board:
        return posts_schema.jsonify(board.posts), 200
    else:
        abort(404, 'No Board.')


# read post
# GET /posts/1
@bp.route('/posts/<int:pid>', methods=['GET'])
@login_required
def detail_view(pid):
    post = Post.query.get(pid)

    if post:
        return post_schema.jsonify(post).data, 200
    else:
        abort(404, 'No Post.')


@bp.route('/boards/<int:bid>/posts/create', methods=['GET'])
@login_required
def create_view(bid):
    board = Board.query.get(bid)
    return board_schema.jsonify(board), 200


# create post
# POST /boards/1/posts
@bp.route('/boards/<int:bid>/posts', methods=['POST'])
@login_required
@use_args(post_schema)
def create(post_args, bid):
    post_args.set_board_id(bid)
    post_args.set_user_id(current_user.id)

    result = post_service.create(post_args)

    return resp_schema.jsonify(result), result['status_code']

    # post_id = result['data']['id']
    # return redirect('/posts/%d'%post_id)


@bp.route('/posts/<int:pid>/update', methods=['GET'])
@login_required
def update_view(pid):
    post = Post.query.get(pid)

    if post:
        return post_schema.jsonify(post).data, 200
    else:
        abort(404, 'No Post.')


# update post
# PATCH /posts/1
@bp.route('/posts/<int:pid>', methods=['PATCH'])
@login_required
@use_args(post_schema)
def update(post_args, pid):
    result = post_service.update(pid, post_args)

    return resp_schema.jsonify(result), result['status_code']


# delete post
# DELETE /posts/1
@bp.route('/posts/<int:pid>', methods=['DELETE'])
@login_required
def delete(pid):
    result = post_service.delete(pid)

    return resp_schema.jsonify(result), result['status_code']