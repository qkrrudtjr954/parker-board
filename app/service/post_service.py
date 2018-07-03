from datetime import datetime

from app.model import db
from app.model.board import Board
from app.model.post import Post
from app.model.user import User


def create(board_id, post: Post, user: User):
    try:
        board = Board.query.get(board_id)
        post.board_id = board.id
        post.user_id = user.id

        db.session.add(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def update(target_post: Post, post_data: Post):
    try:
        target_post.content = post_data.content
        target_post.description = post_data.description
        target_post.title = post_data.title

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def delete(target_post: Post):
    try:
        target_post.delete()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
