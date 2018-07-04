from app.model import db
from app.model.user import User
from app.model.comment import Comment


def create(target_post, comment: Comment, user: User):
    try:
        target_post.increase_comments_count()

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
        comment.delete()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def update(target_comment: Comment, comment_data):
    try:
        target_comment.content = comment_data.content

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
