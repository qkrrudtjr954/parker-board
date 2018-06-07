from tests.factories.board import FakeBoardAndUserFactory
from app.model.board import Board, BoardStatus
from app.schema.board import board_schema
from app.schema.resp import resp_schema
from app.schema.user import login_schema
from app.model.user import User
import pytest


@pytest.fixture(scope='function')
def fboards(tsession):
    board = FakeBoardAndUserFactory.create_batch(10)
    tsession.flush()
    return board


class TestCreateBoard:
    def test_create_board(self, tclient, tsession):
        pass
    #     user = FakeUserFactory()
    #     tsession.flush()
    #
    #     resp = tclient.post('/users/login', data=login_schema.dumps(user).data, content_type='application/json')
    #     result = resp_schema.loads(resp.data.decode()).data
    #     assert resp.status_code == 200
    #
    #     board = FakeBoardFactory.build()
    #     resp = tclient.post('/boards', data=board_schema.dumps(board).data, content_type='application/json')
    #     result = resp_schema.loads(resp.data.decode()).data
    #     assert resp.status_code == 200


class TestReadBoard:
    def test_read_board(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        resp = tclient.get('/')
        result = resp_schema.loads(resp.data.decode()).data

        assert len(result['data']['boards']) == 3


class TestUpdateBoard:
    def test_update_board(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        # login
        login_user = fboards[0].user

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200

        # board update
        board = fboards[0]
        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % board.id, data=board_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 200
        assert board.title == 'changed title'

    def test_update_no_login(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        board = fboards[0]

        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % board.id, data=board_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 400
        assert result['errors']['message'] == 'Login First.'
        assert board.title != 'changed title'

    def test_update_no_auth(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        # login
        login_user = fboards[1].user

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200

        # board update
        board = fboards[0]

        assert login_user != board.user

        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % board.id, data=board_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 401
        assert result['errors']['message'] == 'Can\'t update.'
        assert board.title != 'changed title'


class TestDeleteBoard:
    def test_delete_board(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        # login
        login_user = fboards[0].user

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200

        # board delete
        board = fboards[0]
        resp = tclient.delete('/boards/%d' % board.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 200
        assert board.status == BoardStatus.DELETED
        assert Board.query.filter(Board.status!=2).count() == 9

    def test_delete_no_login(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        # board delete
        board = fboards[0]

        resp = tclient.delete('/boards/%d' % board.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 400
        assert result['errors']['message'] == 'Login First.'
        assert board.status != 2

    def test_delete_no_auth(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        # login
        login_user = fboards[1].user

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200

        # board delete
        board = fboards[0]

        assert board.user != login_user

        resp = tclient.delete('/boards/%d' % board.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 401
        assert result['errors']['message'] == 'Can\'t delete.'
        assert board.status == 0
        assert Board.query.filter(Board.status != 2).count() == 10
