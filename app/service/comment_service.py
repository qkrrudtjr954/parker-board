from app.schema.comment import comment_schema
from app.model.comment import Comment
from app.model import db
from flask_login import current_user


def create(comment, pid):
    result = {}

    comment.set_user_id(current_user.id)
    comment.set_post_id(pid)

    try:
        db.session.add(comment)
        db.session.flush()

        result['data'] = comment_schema.dump(comment).data
        result['status_code'] = 200
    except Exception:
        result['errors'] = dict(error='Server Error. Please Try again.')
        result['status_code'] = 500

    return result


def delete(cid):
    comment = Comment.query.get(cid)
    result = {}

    if comment:
        if current_user.id == comment.user_id:
            comment.change_status()

            db.session.add(comment)
            db.session.flush()

            result['data'] = comment_schema.dump(comment).data
            result['status_code'] = 200
        else:
            result['errors'] = 'Can\'t delete.'
            result['status_code'] = 401
    else:
        result['errors'] = dict(error='No Comment.')
        result['status_code'] = 400

    return result


def update(cid, data):
    comment = Comment.query.get(cid)
    result = {}

    if comment:
        if current_user.id == comment.user_id:
            comment.set_content(data.content if data.content else comment.content)
            comment.set_updated_at()

            db.session.add(comment)
            db.session.flush()

            result['data'] = comment_schema.dump(comment).data
            result['status_code'] = 200
        else:
            result['errors'] = 'Can\'t update.'
            result['status_code'] = 401
    else:
        result['errors'] = dict(error='No Comment.')
        result['status_code'] = 400

    return result
