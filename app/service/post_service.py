from datetime import datetime
from app.model import db
from app.model.board import Board
from app.model.post import Post, PostStatus


def pagination_posts(page, per_page, board_id):
    posts = Post.query\
        .filter(Post.status != PostStatus.DELETED)\
        .filter(Post.board_id == board_id)\
        .order_by(Post.created_at.desc())\
        .paginate(per_page=per_page, error_out=False)
    posts.page = page

    return posts


def get_post(post_id):
    return Post.query.get(post_id)


def create(board_id, post: Post, user):
    try:
        board = Board.query.get(board_id)
        post.board = board
        post.user = user

        db.session.add(post)
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def update(target_post: Post, post_data: Post):
    try:
        target_post.title = post_data.title
        target_post.content = post_data.content
        target_post.description = post_data.description

        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def delete(target_post: Post):
    try:
        target_post.status = PostStatus.DELETED
        target_post.updated_at = datetime.utcnow()

        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e
