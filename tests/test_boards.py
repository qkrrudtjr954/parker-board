from tests.factories.board import FakeBoardFactory
from app.model.board import Board, BoardStatus
from app.schema.board import board_schema
from app.schema.user import user_schema
from app.model.user import User
import pytest
import json


@pytest.fixture(scope='function')
def fboard(tsession):
    board = FakeBoardFactory()
    tsession.flush()
    return board


@pytest.fixture(scope='function')
def fboards(tsession):
    board = FakeBoardFactory.create_batch(10)
    tsession.flush()
    return board


class TestCreateBoard:
    def test_create_board(self, tclient, tsession):
        pass


class TestReadBoard:
    def test_read_board(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        resp = tclient.get('/boards/')

        assert resp.status_code == 200

        result = json.loads(resp.data)

        assert len(result['boards']) == 10

    def test_read_board_페이지_3개(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        resp = tclient.get('/boards/?per_page=3')

        assert resp.status_code == 200

        result = json.loads(resp.data)

        assert len(result['boards']) == 3


class TestUpdateBoard:
    def test_update_board(self, tclient, fboard, tsession):
        assert tsession.query(User).one()
        assert tsession.query(Board).one()

        data = user_schema.dumps(fboard.user).data
        resp = tclient.post('/users/login', data=data, content_type='application/json')
        assert resp.status_code == 200

        # board update
        board = fboard
        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % board.id, data=board_schema.dumps(update_data).data, content_type='application/json')

        assert resp.status_code == 200
        assert board.title == 'changed title'

    def test_update_no_login(self, tclient, fboard):
        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % fboard.id, data=board_schema.dumps(update_data).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 400
        assert result['message'] == 'Login First.'
        assert fboard.title != 'changed title'

    def test_update_no_auth(self, tclient, fboards):
        login_user = fboards[0].user

        resp = tclient.post('/users/login', data=user_schema.dumps(login_user).data, content_type='application/json')
        assert resp.status_code == 200

        update_board = fboards[1]

        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % update_board.id, data=board_schema.dumps(update_data).data, content_type='application/json')

        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'
        assert update_board.title != 'changed title'


class TestDeleteBoard:
    def test_delete_board(self, tclient, fboard):
        resp = tclient.post('/users/login', data=user_schema.dumps(fboard.user).data, content_type='application/json')
        assert resp.status_code == 200

        # board delete
        resp = tclient.delete('/boards/%d' % fboard.id, content_type='application/json')

        assert resp.status_code == 200
        assert fboard.status == BoardStatus.DELETED
        assert Board.query.first().status == BoardStatus.DELETED

    def test_delete_no_login(self, tclient, fboard):
        resp = tclient.delete('/boards/%d' % fboard.id, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 400
        assert result['message'] == 'Login First.'
        assert fboard.title != 'changed title'

    def test_delete_no_auth(self, tclient, fboards):
        login_user = fboards[0].user

        resp = tclient.post('/users/login', data=user_schema.dumps(login_user).data, content_type='application/json')
        assert resp.status_code == 200

        delete_board = fboards[1]
        resp = tclient.delete('/boards/%d' % delete_board.id, content_type='application/json')

        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'
        assert delete_board.status != BoardStatus.DELETED
