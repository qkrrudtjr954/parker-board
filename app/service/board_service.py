from app.schema.board import board_schema, boards_schema
from app.model import db
from app.model.board import Board
from flask_login import current_user


def create(board, user_id):
    result = {}

    try:
        board.user_id = user_id
        db.session.add(board)
        db.session.flush()

        result['data'] = board_schema.dump(board).data
        result['status_code'] = 200

    except Exception:
        db.session.rollback()
        result['errors'] = dict(message='Server Error. Please Try again.')
        result['status_code'] = 500

    return result


def delete(bid):
    board = Board.query.get(bid)
    result = {}

    if board:
        if board.user_id == current_user.id:
            board.deleted()

            db.session.add(board)
            db.session.flush()

            result['data'] = board_schema.dump(board).data
            result['status_code'] = 200
        else:
            result['errors'] = dict(message='Can\'t delete.')
            result['status_code'] = 401
    else:
        result['errors'] = dict(message='No Board.')
        result['status_code'] = 400

    return result


def update(board_id, data, user):
    board = Board.query.get(board_id)
    result = {}

    if board:
        if board.user_id == user.id:

            board.set_title(data.title if data.title else board.title)
            board.set_description(data.description if data.description else board.description)
            board.set_updated_at()

            db.session.add(board)
            db.session.flush()

            result['data'] = board_schema.dump(board).data
            result['status_code'] = 200
        else:
            result['errors'] = dict(message='Can\'t update.')
            result['status_code'] = 401
    else:
        result['errors'] = dict(message='No Board.')
        result['status_code'] = 400

    return result
