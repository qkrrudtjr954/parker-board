from flask import Blueprint, jsonify, abort
from webargs.flaskparser import use_args

from app.schema.like import is_liked_schema
from app.schema.error import default_message_error_schema
from app.service import post_service
from app.model.board import Board
from app.model.post import Post
from app.schema.post import main_post_schema, post_create_form_schema, post_update_form_schema, post_id_schema, \
    post_like_count_schema, post_list_schema
from app.schema.pagination import pagination_schema
from flask_login import login_required, current_user

bp = Blueprint('post', __name__)


'''
글
목록, 생성, 삭제, 수정, 읽기
'''

# list post
# GET /boards/1/posts
@bp.route('/boards/<int:board_id>/posts', methods=['GET'])
@use_args(pagination_schema)
def post_list(pagination, board_id):
    board = Board.query.get(board_id)

    if not board:
        error = dict(message='존재하지 않는 게시판 입니다.')
        return default_message_error_schema.jsonify(error), 404

    posts_data = board.posts\
        .filter(~Post.is_deleted)\
        .order_by(Post.created_at.desc())\
        .paginate(page=pagination.page, per_page=pagination.per_page, error_out=False)

    post_list = post_list_schema.dump(posts_data.items).data
    total_count = posts_data.total

    result = dict(post_list=post_list, total_count=total_count)

    return jsonify(result), 200


# read post
# GET /posts/1
@bp.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def detail(post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        error = dict(message='존재하지 않는 게시글 입니다.')
        return default_message_error_schema.jsonify(error), 404

    target_post.read()

    return main_post_schema.jsonify(target_post), 200


# create post
# POST /boards/1/posts
@bp.route('/boards/<int:board_id>/posts', methods=['POST'])
@login_required
@use_args(post_create_form_schema)
def create(post: Post, board_id):
    try:
        post_service.create(board_id, post, current_user)
        return post_id_schema.jsonify(post), 200
    except Exception as e:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500


# update post
# PATCH /posts/1
@bp.route('/posts/<int:post_id>', methods=['PATCH'])
@login_required
@use_args(post_update_form_schema)
def update(post_data, post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        error = dict(message='존재하지 않는 게시글 입니다.')
        return default_message_error_schema.jsonify(error), 404

    if not target_post.is_owner(current_user):
        error = dict(message='권한이 없습니다.')
        return default_message_error_schema.jsonify(error), 401

    try:
        post_service.update(target_post, post_data)
        return post_id_schema.jsonify(target_post), 200
    except Exception:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500


# delete post
# DELETE /posts/1
@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete(post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        error = dict(message='존재하지 않는 게시글 입니다.')
        return default_message_error_schema.jsonify(error), 404

    if not target_post.is_owner(current_user):
        error = dict(message='권한이 없습니다.')
        return default_message_error_schema.jsonify(error), 401

    try:
        post_service.delete(target_post)
        return post_id_schema.jsonify(target_post), 204
    except Exception:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500


@bp.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like(post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        error = dict(message='존재하지 않는 게시글 입니다.')
        return default_message_error_schema.jsonify(error), 404
    
    target_post.like(current_user)
    result = dict(like_count=target_post.like_count)

    return post_like_count_schema.jsonify(result), 200


@bp.route('/posts/<int:post_id>/unlike', methods=['POST'])
@login_required
def unlike(post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        error = dict(message='존재하지 않는 게시글 입니다.')
        return default_message_error_schema.jsonify(error), 404

    target_post.unlike(current_user)
    result = dict(like_count=target_post.like_count)

    return post_like_count_schema.jsonify(result), 200


@bp.route('/posts/<int:post_id>/is-liked', methods=['GET'])
@login_required
def is_liked(post_id):
    result = dict(is_liked=current_user.is_liked(post_id))
    return is_liked_schema.jsonify(result), 200

