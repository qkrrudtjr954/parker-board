from app.model import db
from app.model.board import Board

from app.model.user import User


def create(user: User, board: Board):
    try:
        board.user_id = user.id

        db.session.add(board)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e


def update(target_board: Board, board_data: Board):
    try:
        if target_board.title != board_data.title:
            target_board.title = board_data.title

        if target_board.description != board_data.description:
            target_board.description = board_data.description

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e


def delete(board: Board):
    try:
        board.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e