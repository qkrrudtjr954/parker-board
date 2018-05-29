from parker_board.model.post import Post
from parker_board.schema.post import post_schema, posts_schema
from parker_board.schema.comment import comments_schema
from parker_board.model import db
from flask import session


from parker_board.service import board_service


def create(board, post):
    result = {}

    current_user = session.get('current_user')

    # 유저 없으면 종료
    if current_user is None:
        result['message'] = 'Session expried. Please Login.'
        result['status_code'] = 401

        return result

    # 유저 있으면 board 객체 생성
    post.set_user_id(current_user['id'])
    post.set_board_id(board.id)

    # 생성되면 디비 세션에 저장
    db.session.add(post)

    # 커밋
    db.session.commit()

    result['message'] = post_schema.dump(post).data
    result['status_code'] = 200

    return result


def get(pid):
    post = Post.query.get(pid)
    result = {}

    if post:
        result['message'] = post_schema.dump(post).data
        result['message']['comments'] = comments_schema.dump(post.comments).data
        result['status_code'] = 200
    else:
        result['message'] = 'No Post.'
        result['status_code'] = 400

    return result


# def update(pid, data):


def delete(pid):
    result = {}

    current_user = session.get('current_user')

    # 유저 없으면 종료
    if current_user is None:
        result['message'] = 'Session expried. Please Login.'
        result['status_code'] = 401
    else:
        # 유저 권한 검사 들어가야함.
        del_count = Post.query.filter_by(id=pid).delete()

        if del_count:
            result['message'] = 'Post deleted'
            result['status_code'] = 204
            db.session.commit()
        else:
            result['message'] = 'No Post.'
            result['status_code'] = 400

    return result


def list(bid):
    board = board_service.get(bid)
    result = {}

    if board:
        result['message'] = posts_schema.dump(board.posts).data
        result['status_code'] = 200
    else:
        result['message'] = 'No Board'
        result['status_code'] = 400

    return result
