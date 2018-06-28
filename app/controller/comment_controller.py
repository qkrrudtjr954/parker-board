from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from webargs.flaskparser import use_args

from app.error import NotFoundError, SameDataError
from app.model.comment import Comment
from app.model.post import Post
from app.schema.pagination import pagination_schema
from app.service import comment_service
from app.schema.comment import comment_create_form_schema, comment_update_form_schema, after_updated_schema, \
    after_create_schema, comment_schema, comments_schema

bp = Blueprint('comment', __name__)

'''
댓글 
생성, 삭제, 수정
'''

@bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@use_args(pagination_schema)
@login_required
def comment_list(pagination, post_id):
    target_post: Post= Post.query.get(post_id)

    if not target_post:
        return 'No Post', 404

    comments_data = target_post.get_comments(pagination.page, pagination.per_page)

    comment_list = comments_schema.dump(comments_data.items).data
    total_count = comments_data.total

    result = dict(comment_list=comment_list, total_count=total_count)
    return jsonify(result), 200

@bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
@use_args(comment_create_form_schema)
def create(comment, post_id):
    try:
        comment_service.create(post_id, comment, current_user)

        return after_create_schema.jsonify(comment), 200
    except NotFoundError as e:
        return str(e), 404
    except Exception:
        return 'Server Error.', 500


@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete(comment_id):
    comment = Comment.query.get(comment_id)

    if not comment:
        return 'No Comment.', 404

    if comment.user_id != current_user.id:
        return 'No Authentication.', 401

    try:
        comment_service.delete(comment)
        return 'Comment deleted', 204
    except Exception:
        return 'Server Error.', 500


@bp.route('/comments/<int:comment_id>', methods=['PATCH'])
@login_required
@use_args(comment_update_form_schema)
def update(comment_data, comment_id):
    target_comment = Comment.query.get(comment_id)

    if not target_comment:
        return 'No Comment.', 404

    if target_comment.user_id != current_user.id:
        return 'No Authentication.', 401

    try:
        comment_service.update(target_comment, comment_data)
        return after_updated_schema.jsonify(target_comment), 200
    except SameDataError as e:
        return str(e), 406
    except Exception:
        return 'Server Error.', 500
