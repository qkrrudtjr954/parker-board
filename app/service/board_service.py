from app.model import db
from app.model.board import Board, BoardStatus
from datetime import datetime


def pagination_boards(page, per_page):
    boards = Board.query.filter(Board.status != BoardStatus.DELETED).order_by(Board.created_at.desc()).paginate(per_page=per_page, error_out=False)
    boards.page = page

    return boards


def create(board: Board, user):
    try:
        board.user_id = user.id

        db.session.add(board)
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def update(target_board: Board, board_data: Board):
    try:
        target_board.title = board_data.title
        target_board.description = board_data.description

        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def delete(board: Board):
    try:
        board.status = BoardStatus.DELETED
        board.updated_at = datetime.utcnow()
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def get_board(board_id):
    return Board.query.get(board_id)
