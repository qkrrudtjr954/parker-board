from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from webargs.flaskparser import use_args

from app import User
from app.model.comment import Comment
from app.model.comment_group import CommentGroup
from app.model.post import Post
from app.schema.error import default_message_error_schema
from app.schema.pagination import pagination_schema
from app.service import comment_service
from app.schema.comment import comment_create_form_schema, comment_update_form_schema, after_updated_schema, \
    after_create_schema, comment_list_schema, layer_comment_create_form
from flask_login import login_required

bp = Blueprint('comment', __name__)

'''
댓글 
생성, 삭제, 수정
'''


@bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@login_required
@use_args(pagination_schema)
def get_comment_list(pagination, post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        error = dict(message='존재하지 않는 게시글 입니다.')
        return default_message_error_schema.jsonify(error), 404

    paged_data = Comment.query\
        .join(CommentGroup)\
        .filter(CommentGroup.post_id == post_id)\
        .filter(Comment.comment_group_id == CommentGroup.id)\
        .order_by(Comment.comment_group_id.desc())\
        .order_by(Comment.step.asc())\
        .paginate(page=pagination.page, per_page=pagination.per_page, error_out=False)

    comment_list = comment_list_schema.dump(paged_data.items).data
    total = paged_data.total

    return jsonify(dict(comment_list=comment_list, total=total)), 200


@bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
@use_args(comment_create_form_schema)
def create_comment(comment, post_id):
    target_post = Post.query.get(post_id)

    if not target_post:
        error = dict(message='존재하지 않는 게시글 입니다.')
        return default_message_error_schema.jsonify(error), 404

    try:
        new_comment = comment_service.add_comment(target_post=target_post,
                                                  comment=comment,
                                                  user=current_user)
    except Exception as e:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500

    return after_create_schema.jsonify(new_comment), 200


@bp.route('/comment_groups/<int:group_id>/comments', methods=['POST'])
@login_required
@use_args(layer_comment_create_form)
def create_layer_comment(comment, group_id):
    target_group = CommentGroup.query.get(group_id)

    if not target_group:
        error = dict(message='댓글 그룹이 존재하지 않습니다.')
        return default_message_error_schema.jsonify(error), 404

    parent_comment = target_group.get_comment_in_group(comment.parent_id)

    if not parent_comment:
        error = dict(message='부모 댓글이 존재하지 않습니다.')
        return default_message_error_schema.jsonify(error), 404

    try:
        new_comment = comment_service.add_layer_comment(target_group=target_group,
                                                        parent_comment=parent_comment,
                                                        comment=comment,
                                                        user=current_user)

    except Exception:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500

    return after_create_schema.jsonify(new_comment), 200


@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    target_comment = Comment.query.get(comment_id)

    if not target_comment:
        error = dict(message='존재하지 않는 댓글 입니다.')
        return default_message_error_schema.jsonify(error), 404

    if not target_comment.is_owner(current_user):
        error = dict(message='권한이 없습니다.')
        return default_message_error_schema.jsonify(error), 401

    try:
        comment_service.delete(target_comment)
        return 'Comment deleted', 204

    except Exception:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500


@bp.route('/comments/<int:comment_id>', methods=['PATCH'])
@use_args(comment_update_form_schema)
@login_required
def update_comment(update_data, comment_id):
    target_comment = Comment.query.get(comment_id)

    if not target_comment or target_comment.is_deleted:
        error = dict(message='존재하지 않는 댓글 입니다.')
        return default_message_error_schema.jsonify(error), 404

    if not target_comment.is_owner(current_user):
        error = dict(message='권한이 없습니다.')
        return default_message_error_schema.jsonify(error), 401

    try:
        comment_service.update(target_comment, update_data)
        return after_updated_schema.jsonify(target_comment), 200
    except Exception:
        error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
        return default_message_error_schema.jsonify(error), 500
# @bp.route('/posts/<int:post_id>/comments', methods=['GET'])
# @use_args(pagination_schema)
# @login_required
# def comment_list(pagination, post_id):
#     target_post: Post = Post.query.get(post_id)
#
#     if not target_post:
#         error = dict(message='존재하지 않는 게시글 입니다.')
#         return default_message_error_schema.jsonify(error), 404
#
#     comments_data = target_post.comments\
#         .filter(
#             ~Comment.is_deleted
#         ).order_by(
#             Comment.created_at.desc()
#         ).paginate(
#             page=pagination.page, per_page=pagination.per_page, error_out=False)
#
#     comment_list = comments_schema.dump(comments_data.items).data
#     total_count = comments_data.total
#
#     result = dict(comment_list=comment_list, total_count=total_count)
#     return jsonify(result), 200
#
# @bp.route('/posts/<int:post_id>/comments', methods=['POST'])
# @login_required
# @use_args(comment_create_form_schema)
# def create(comment, post_id):
#     target_post = Post.query.get(post_id)
#     if not target_post:
#         error = dict(message='존재하지 않는 게시글 입니다.')
#         return default_message_error_schema.jsonify(error), 404
#
#     try:
#         comment_service.create(target_post, comment, current_user)
#         return after_create_schema.jsonify(comment), 200
#     except Exception:
#         error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
#         return default_message_error_schema.jsonify(error), 500
#
#
# @bp.route('/comments/<int:comment_id>', methods=['DELETE'])
# @login_required
# def delete(comment_id):
#     target_comment = Comment.query.get(comment_id)
#
#     if not target_comment:
#         error = dict(message='존재하지 않는 댓글 입니다.')
#         return default_message_error_schema.jsonify(error), 404
#
#     if not target_comment.is_owner(current_user):
#         error = dict(message='권한이 없습니다.')
#         return default_message_error_schema.jsonify(error), 401
#
#     try:
#         comment_service.delete(target_comment)
#         return 'Comment deleted', 204
#
#     except Exception:
#         error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
#         return default_message_error_schema.jsonify(error), 500
#
#
# @bp.route('/comments/<int:comment_id>', methods=['PATCH'])
# @login_required
# @use_args(comment_update_form_schema)
# def update(comment_data, comment_id):
#     target_comment = Comment.query.get(comment_id)
#
#     if not target_comment:
#         error = dict(message='존재하지 않는 댓글 입니다.')
#         return default_message_error_schema.jsonify(error), 404
#
#     if not target_comment.is_owner(current_user):
#         error = dict(message='권한이 없습니다.')
#         return default_message_error_schema.jsonify(error), 401
#
#     try:
#         comment_service.update(target_comment, comment_data)
#         return after_updated_schema.jsonify(target_comment), 200
#     except Exception:
#         error = dict(message='서버상의 문제가 발생했습니다. 다시 시도해주세요.')
#         return default_message_error_schema.jsonify(error), 500
