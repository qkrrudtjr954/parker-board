from app.model import db
from app.model.board import Board, BoardStatus

from app.model.user import User


def pagination_boards(page, per_page):
    boards = Board.query\
        .filter(Board.status != BoardStatus.DELETED)\
        .order_by(Board.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return boards


def create(user: User, board: Board):
    try:
        board.user_id = user.id

        db.session.add(board)
        db.session.flush()

    except Exception as e:
        db.session.rollback()
        raise e


def update(target_board: Board, board_data: Board):
    try:
        if target_board.title != board_data.title:
            target_board.title = board_data.title

        if target_board.description != target_board.description:
            target_board.description = board_data.description

        target_board.refresh_update_time()

        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e


def delete(board: Board):
    try:
        board.deleted()
        board.refresh_update_time()

        db.session.flush()
    except Exception as e:
        db.session.rollback()
        raise e