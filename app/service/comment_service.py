from datetime import datetime
from app.model import db
from app.model.user import User
from app.model.post import Post
from app.model.comment import Comment, CommentStatus


def create(post_id, comment: Comment, user: User):
    try:
        target_post = Post.query.get(post_id)
        comment.user_id = user.id
        comment.post_id = target_post.id

        db.session.add(comment)
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def get_comment(comment_id):
    return Comment.query.get(comment_id)


def delete(comment: Comment):
    try:
        comment.status = CommentStatus.DELETED

        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def update(target_comment: Comment, comment_data: Comment):
    try:
        target_comment.content = comment_data.content
        target_comment.updated_at = datetime.utcnow()

        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e
