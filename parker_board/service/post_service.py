from parker_board.model.post import Post
from parker_board.model.board import Board
from parker_board.schema.post import post_schema, posts_schema
from parker_board.schema.comment import comments_schema
from parker_board.model import db
from flask_login import current_user


def create(post):
    result = {}
    try:
        db.session.add(post)
        db.session.commit()

        result['data'] = post_schema.dump(post).data
        result['status_code'] = 200
    except Exception:
        db.session.rollback()

        result['errors'] = dict(error='Server Error.')
        result['status_code'] = 500

    return result


def delete(pid):
    result = {}

    # 유저 없으면 종료
    if current_user is None:
        result['message'] = 'Session expried. Please Login.'
        result['status_code'] = 401
    else:
        # 유저 권한 검사 들어가야함.
        del_count = Post.query.filter_by(id=pid).delete()

        if del_count:
            result['message'] = 'Post deleted'
            result['status_code'] = 204
            db.session.commit()
        else:
            result['message'] = 'No Post.'
            result['status_code'] = 400

    return result


def update(pid, data):
    post = Post.query.get(pid)
    result = {}

    if post:
        post.set_title(data.title if data.title else post.title)
        post.set_description(data.description if data.description else post.description)
        post.set_content(data.content if data.content else post.content)
        post.set_updated_at()

        db.session.add(post)
        db.session.commit()

        result['data'] = post_schema.dump(post).data
        result['status_code'] = 200
    else:
        result['errors'] = dict(error='No Post.')
        result['status_code'] = 400

    return result