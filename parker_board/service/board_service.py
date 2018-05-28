from flask import session
from parker_board.schema.board import board_schema
from parker_board.model import db


def add_board(board):
    result = {}

    # session 에서 유저를 가져온다.
    current_user = session.get('current_user')

    # 유저 없으면 종료
    if current_user is None:
        result['message'] = 'Session expried. Please Login.'
        result['status_code'] = 401

        return result

    # 유저 있으면 board 객체 생성
    board.user_id = current_user['id']

    # 생성되면 디비 세션에 저장
    db.session.add(board)

    # 커밋
    db.session.commit()

    result['message'] = board_schema.dump(board).data
    result['status_code'] = 200

    return result
