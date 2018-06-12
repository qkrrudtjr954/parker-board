from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from app.service import post_service
from app.model.board import Board
from app.model.post import Post
from app.schema.board import simple_board_schema
from app.schema.post import main_post_schema, before_create_post_schema, before_update_post_schema, after_create_post_schema, after_update_post_schema, after_delete_post_schema, post_list_schema
from app.schema.comment import comments_schema
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
@login_required
def post_view(pagination, board_id):
    board = Board.query.get(board_id)

    if not board:
        return 'No Board.', 400

    posts = board.get_posts(pagination.page, pagination.per_page)

    board_item = simple_board_schema.dump(board).data
    posts_item = post_list_schema.dump(posts.items).data
    pagination = pagination_schema.dump(posts).data

    result = dict(board=board_item, posts=posts_item, pagination=pagination)

    return jsonify(result), 200


# read post
# GET /posts/1
@bp.route('/posts/<int:post_id>', methods=['GET'])
@use_args(pagination_schema)
@login_required
def detail_view(pagination, post_id):

    post = Post.query.get(post_id)

    if not post:
        return 'No Post.', 400

    comments = post.get_comments(pagination.page, pagination.per_page)

    comments_item = comments_schema.dump(comments.items).data
    pagination = pagination_schema.dump(comments).data

    result = dict(post=main_post_schema.dump(post).data, comments=comments_item, pagination=pagination)
    return jsonify(result), 200


# create post
# POST /boards/1/posts
@bp.route('/boards/<int:board_id>/posts', methods=['POST'])
@login_required
@use_args(before_create_post_schema)
def create(post: Post, board_id):
    try:
        post_service.create(board_id, post, current_user)
        return after_create_post_schema.jsonify(post), 200
    except Exception as e:
        return str(e), 500


# update post
# PATCH /posts/1
@bp.route('/posts/<int:post_id>', methods=['PATCH'])
@login_required
@use_args(before_update_post_schema)
def update(post_data: Post, post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        return 'No Post.', 400

    if target_post.user_id != current_user.id:
        return 'No Authentication.', 401

    try:
        post_service.update(target_post, post_data)
        return after_update_post_schema.jsonify(target_post), 200
    except Exception:
        return 'Server Error.', 500


# delete post
# DELETE /posts/1
@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete(post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        return 'No Post.', 400

    if not target_post.user_id == current_user.id:
        return 'No Authentication.', 401

    try:
        post_service.delete(target_post)
        return after_delete_post_schema.jsonify(target_post), 200
    except Exception:
        return 'Server Error.', 500
