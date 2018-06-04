from parker_board.model.post import Post
from parker_board.model.comment import Comment
from parker_board.schema.post import post_schema
from parker_board.model import db
from flask_login import current_user


def read(pid):
    post = Post.query.get(pid)
    result = {}

    if post:
        if post.status == 2:
            result['errors'] = 'Deleted Post.'
            result['status_code'] = 400
        else:
            result['data'] = post_schema.dump(post).data
            result['status_code'] = 200
    else:
        result['errors'] = 'No Post.'
        result['status_code'] = 404

    return result


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
    post = Post.query.get(pid)
    result = {}

    if post:
        if post.user_id == current_user.id:
            post.change_status()

            db.session.add(post)
            db.session.commit()

            result['data'] = post_schema.dump(post).data
            result['status_code'] = 204
        else:
            result['errors'] = 'Can\'t delete.'
            result['status_code'] = 401
    else:
        result['errors'] = dict(error='No Post.')
        result['status_code'] = 404

    return result


def update(pid, data):
    post = Post.query.get(pid)
    result = {}

    if post:
        if post.user_id == current_user.id:
            post.set_title(data.title if data.title else post.title)
            post.set_description(data.description if data.description else post.description)
            post.set_content(data.content if data.content else post.content)
            post.set_updated_at()

            db.session.add(post)
            db.session.commit()

            result['data'] = post_schema.dump(post).data
            result['status_code'] = 200
        else:
            result['errors'] = 'Can\'t update.'
            result['status_code'] = 401
    else:
        result['errors'] = dict(error='No Post.')
        result['status_code'] = 404

    return result
