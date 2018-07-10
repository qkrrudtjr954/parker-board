from app import User
from app.model.comment import Comment
from app.model.comment_group import CommentGroup
from app.model.post import Post


def add_comment(target_post: Post, user: User, comment: Comment):
    target_group = target_post.add_comment_group()

    try:
        # new_comment_group은 group에 댓글을 추가하는 책임을 수행한다.
        new_comment = target_group.add_comment(user=user, comment=comment)
    except Exception as e:
        raise e

    return new_comment


# 계층 댓글을 생성하는 책임
def add_layer_comment(target_group: CommentGroup, comment: Comment, user: User, parent_comment: Comment):
    try:
        new_comment = target_group.add_layer_comment(comment=comment, user=user, parent_comment=parent_comment)

    except Exception as e:
        raise e

    return new_comment


def delete(target_comment: Comment):
    try:
        target_comment.delete()
    except Exception as e:
        raise e


# from app.model import db
# from app.model.user import User
# from app.model.comment import Comment
#
#
# def create(target_post, comment: Comment, user: User):
#     try:
#         target_post.increase_comments_count()
#
#         comment.user_id = user.id
#         comment.post_id = target_post.id
#
#         db.session.add(comment)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e
#
#
# def get_comment(comment_id):
#     return Comment.query.get(comment_id)
#
#
# def delete(comment: Comment):
#     try:
#         comment.delete()
#
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e
#
#
# def update(target_comment: Comment, comment_data):
#     try:
#         target_comment.content = comment_data.content
#
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e
def update(target_comment, data):
    try:
        target_comment.update(data.content)
    except Exception as e:
        raise e