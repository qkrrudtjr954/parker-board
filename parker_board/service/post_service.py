from parker_board.model.post import Post
from parker_board.schema.post import post_schema
from parker_board.model import db
from flask import session


def add_post(board, post):
    result = {}

    current_user = session.get('current_user')

    # 유저 없으면 종료
    if current_user is None:
        result['message'] = 'Session expried. Please Login.'
        result['status_code'] = 401

        return result

    # 유저 있으면 board 객체 생성
    post.user_id = current_user['id']
    post.board_id = board.id

    # 생성되면 디비 세션에 저장
    db.session.add(post)

    # 커밋
    db.session.commit()

    result['message'] = post_schema.dump(post).data
    result['status_code'] = 200

    return result
