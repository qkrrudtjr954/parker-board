from flask import session
from parker_board.schema.comment import comment_schema
from parker_board.model.comment import Comment
from parker_board.model import db


def create(comment, pid):
    result = {}

    current_user = session.get('current_user')

    if current_user is None:
        result['message'] = 'Session expried. Please Login.'
        result['status_code'] = 401

        return result

    comment.set_user_id(current_user['id'])
    comment.set_post_id(pid)

    db.session.add(comment)

    db.session.commit()

    result['message'] = comment_schema.dump(comment).data
    result['status_code'] = 200

    return result


def delete(cid):
    result = {}

    current_user = session.get('current_user')

    # 유저 없으면 종료
    if current_user is None:
        result['message'] = 'Session expried. Please Login.'
        result['status_code'] = 401
    else:
        # 유저 권한 검사 들어가야함.
        del_count = Comment.query.filter_by(id=cid).delete()

        if del_count:
            result['message'] = 'Comment deleted'
            result['status_code'] = 204
            db.session.commit()
        else:
            result['message'] = 'No Comment.'
            result['status_code'] = 400

    return result
