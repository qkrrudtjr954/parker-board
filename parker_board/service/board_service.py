from parker_board.schema.board import board_schema, boards_schema
from parker_board.schema.post import posts_schema
from parker_board.model import db
from parker_board.model.board import Board
from flask_login import current_user


def create(board):
    result = False

    try:
        db.session.add(board)
        db.session.commit()
        result = True
    except Exception:
        db.session.rollback()

    return result


def delete(bid):
    board = Board.query.get(bid)
    result = {}

    if board:
        board.change_status()

        db.session.add(board)
        db.session.commit()

        result['data'] = board_schema.dump(board).data
        result['status_code'] = 200
    else:
        result['errors'] = dict(error='No Board.')
        result['status_code'] = 400

    return result


def update(bid, data):
    board = Board.query.get(bid)
    result = {}

    if board:
        board.set_title(data.title if data.title else board.title)
        board.set_description(data.description if data.description else board.description)
        board.set_updated_at()

        db.session.add(board)
        db.session.commit()

        result['data'] = board_schema.dump(board).data
        result['status_code'] = 200
    else:
        result['errors'] = dict(error='No Board.')
        result['status_code'] = 400

    return result
