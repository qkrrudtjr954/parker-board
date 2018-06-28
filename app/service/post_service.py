from datetime import datetime

from app.error import SameDataError
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


def update(target_post: Post, post_data):

    if target_post.is_same_data(post_data):
        raise SameDataError('Nothing Changed. Same data.')

    try:
        changed = False

        if 'title' in post_data and target_post.title != post_data['title']:
            target_post.title = post_data['title']
            changed = True

        if 'description' in post_data and target_post.description != post_data['description']:
            target_post.description = post_data['description']
            changed = True

        if 'content' in post_data and target_post.content != post_data['content']:
            target_post.content = post_data['content']
            changed = True

        if changed:
            target_post.refresh_update_time()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def delete(target_post: Post):
    try:
        target_post.deleted()
        target_post.updated_at = datetime.utcnow()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
