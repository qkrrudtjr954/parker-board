from parker_board.model.post import Post
from parker_board.schema.post import post_schema
from parker_board.model import db


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
        post.change_status()

        db.session.add(post)
        db.session.commit()

        result['data'] = post_schema.dump(post).data
        result['status_code'] = 204
    else:
        result['errors'] = dict(error='No Post.')
        result['status_code'] = 404

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
        result['status_code'] = 404

    return result
