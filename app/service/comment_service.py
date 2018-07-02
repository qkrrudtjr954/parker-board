from datetime import datetime

from app.error import NotFoundError, SameDataError
from app.model import db
from app.model.user import User
from app.model.post import Post
from app.model.comment import Comment


def create(post_id, comment: Comment, user: User):
    target_post = Post.query.get(post_id)

    if not target_post:
        raise NotFoundError('No Post.')

    try:
        target_post.comments_count = target_post.comments_count + 1

        comment.user_id = user.id
        comment.post_id = target_post.id

        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def get_comment(comment_id):
    return Comment.query.get(comment_id)


def delete(comment: Comment):
    try:
        comment.post.comments_count = comment.post.comments_count - 1
        comment.delete()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def update(target_comment: Comment, comment_data):
    if target_comment.content == comment_data.content:
        raise SameDataError('Nothing Changed. Same data.')

    try:
        target_comment.content = comment_data.content

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
