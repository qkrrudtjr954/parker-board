from parker_board.schema.comment import comment_schema
from parker_board.model.comment import Comment
from parker_board.model import db


def create(comment):
    result = {}

    try:
        db.session.add(comment)
        db.session.commit()

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
        comment.change_status()

        db.session.add(comment)
        db.session.commit()

        result['data'] = comment_schema.dump(comment).data
        result['status_code'] = 200
    else:
        result['errors'] = dict(error='No Comment.')
        result['status_code'] = 400

    return result


def update(cid, data):
    comment = Comment.query.get(cid)
    result = {}

    if comment:
        comment.set_content(data.content if data.content else comment.content)
        comment.set_updated_at()

        db.session.add(comment)
        db.session.commit()

        result['data'] = comment_schema.dump(comment).data
        result['status_code'] = 200
    else:
        result['errors'] = dict(error='No Comment.')
        result['status_code'] = 400

    return result
