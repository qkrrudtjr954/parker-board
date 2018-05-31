from parker_board.schema.board import board_schema, boards_schema
from parker_board.schema.post import posts_schema
from parker_board.model import db
from parker_board.model.board import Board


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
    del_count = Board.query.filter_by(id=bid).delete()
    result = {}

    if del_count:
        result['message'] = 'Board deleted.'
        result['status_code'] = 204

        db.session.commit()
    else:
        result['message'] = 'No Board.'
        result['status_code'] = 400

    return result


def get(bid):
    board = Board.query.get(bid)
    result = {}

    if board:
        result['message'] = board_schema.dump(board).data
        result['message']['posts'] = posts_schema.dump(board.posts).data
        result['status_code'] = 200
    else:
        result['message'] = 'No Board.'
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

        result['message'] = board_schema.dump(board).data
        result['message']['posts'] = posts_schema.dump(board.posts).data
        result['status_code'] = 200
    else:
        result['message'] = 'No Board.'
        result['status_code'] = 400

    return result


def list():
    boards = Board.query.all()
    result = dict(message= boards_schema.dump(boards).data, status_code= 200)

    return result