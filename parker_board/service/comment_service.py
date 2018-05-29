from flask import session
from parker_board.model.board import Board
from parker_board.model.post import Post
from parker_board.schema.comment import comments_schema, comment_schema
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
    pass