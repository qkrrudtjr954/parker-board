from flask import Blueprint
from webargs.flaskparser import use_args

from app.model.comment import Comment
from app.schema.comment import comment_schema
from app.service import comment_service
from app.schema.resp import resp_schema
from flask_login import current_user, login_required


bp = Blueprint('comment', __name__)

'''
댓글 
생성, 삭제, 수정
'''


@bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
@use_args(comment_schema)
def create(comment, post_id):
    try:
        comment_service.create(post_id, comment, current_user)
        return comment_schema.jsonify(comment), 200
    except Exception:
        return 'Server Error.', 500


@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete(comment_id):
    comment = Comment.query.get(comment_id)

    if comment:
        comment_service.delete(comment)
        return comment_schema.jsonify(comment), 200
    else:
        return 'No Comment.', 400


@bp.route('/comments/<int:comment_id>', methods=['PATCH'])
@login_required
@use_args(comment_schema)
def update(comment_data, comment_id):
    target_comment = Comment.query.get(comment_id)

    if not target_comment:
        return 'No Comment.', 400

    if target_comment.user_id != current_user.id:
        return 'No Authentication.', 401

    try:
        comment_service.update(target_comment, comment_data)
        return comment_schema.jsonify(target_comment), 200
    except Exception:
        return 'Server Error.', 500
