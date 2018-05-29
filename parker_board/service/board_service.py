from flask import session
from parker_board.schema.board import board_schema
from parker_board.model import db
from parker_board.model.board import Board


def create(board):
    result = {}

    # session 에서 유저를 가져온다.
    current_user = session.get('current_user')

    # 유저 없으면 종료
    if current_user is None:
        result['message'] = 'Session expried. Please Login.'
        result['status_code'] = 401

        return result

    # 유저 있으면 board 객체 생성
    board.set_user_id(current_user['id'])

    # 생성되면 디비 세션에 저장
    db.session.add(board)

    # 커밋
    db.session.commit()

    result['message'] = board_schema.dump(board).data
    result['status_code'] = 200

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


def get(board_id):
    return Board.query.get(board_id)


def list():
    return Board.query.all()


# def update_board(board_id, data):
#     result = {}
#     result['message'] = 'update.'
#     result['status_code'] = 200
