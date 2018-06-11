from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from app.service import post_service, comment_service
from app.model.post import Post
from app.schema.post import post_schema, main_post_schema, main_posts_schema
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
@bp.route('/boards/<int:board_id>/posts/', methods=['GET'])
@use_args(pagination_schema)
@login_required
def post_view(pagination, board_id):
    posts = post_service.pagination_posts(pagination.page, pagination.per_page, board_id)

    posts_item = main_posts_schema.dump(posts.items).data
    pagination = pagination_schema.dump(posts).data

    result = dict(posts=posts_item, pagination=pagination)

    return jsonify(result), 200


# read post
# GET /posts/1
@bp.route('/posts/<int:post_id>', methods=['GET'])
@use_args(pagination_schema)
@login_required
def detail_view(pagination, post_id):
    # comments = post_service.get_comments(post_id, pagination.page, pagination.per_page)

    post = post_service.get_post(post_id)

    if post:
        comments = post.get_comments(pagination.page, pagination.per_page)
        # comments = comment_service.pagination_comments(pagination.page, pagination.per_page, post_id)

        comments_item = comments_schema.dump(comments.items).data
        pagination = pagination_schema.dump(comments).data

        result = dict(post=main_post_schema.dump(post).data, comments=comments_item, pagination=pagination)
        return jsonify(result), 200
    else:
        return 'No Post.', 400


# create post
# POST /boards/1/posts
@bp.route('/boards/<int:board_id>/posts', methods=['POST'])
@login_required
@use_args(post_schema)
def create(post: Post, board_id):
    try:
        post_service.create(board_id, post, current_user)
        return post_schema.jsonify(post), 200
    except Exception:
        return 'Server Error.', 500


# update post
# PATCH /posts/1
@bp.route('/posts/<int:post_id>', methods=['PATCH'])
@login_required
@use_args(post_schema)
def update(post_data: Post, post_id):
    # post_service.update(post_id, post_data, current_user)
    target_post = Post.query.get(post_id)

    if not target_post:
        return 'No Post.', 400

    if target_post.user_id != current_user.id:
        return 'No Authentication.', 401

    try:
        post_service.update(target_post, post_data)
        return post_schema.jsonify(target_post), 200
    except Exception:
        return 'Server Error.', 500


# delete post
# DELETE /posts/1
@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete(post_id):
    target_post = post_service.get_post(post_id)

    if target_post:
        if target_post.user_id == current_user.id:
            try:
                post_service.delete(target_post)
                return post_schema.jsonify(target_post), 200
            except Exception:
                return 'Server Error.', 500
        else:
            return 'No Authentication.', 401
    else:
        return 'No Post.', 400

