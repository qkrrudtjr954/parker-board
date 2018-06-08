from tests.factories.board import FakeBoardFactory
from app.model.board import Board, BoardStatus
from app.schema.board import board_schema
from app.schema.resp import resp_schema
from app.schema.user import user_schema, login_schema
from app.model.user import User
import pytest


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

        resp = tclient.get('/')
        result = resp_schema.loads(resp.data.decode()).data

        assert len(result['data']['boards']) == 3


class TestUpdateBoard:
    def test_update_board(self, tclient, fboard, tsession):
        assert tsession.query(User).one()
        assert tsession.query(Board).one()

        data = user_schema.dumps(fboard.user).data
        resp = tclient.post('/users/login', data=data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200

        # board update
        board = fboard
        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % board.id, data=board_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 200
        assert board.title == 'changed title'

    def test_update_no_login(self, tclient, fboard):
        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % fboard.id, data=board_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 400
        assert result['errors']['message'] == 'Login First.'
        assert fboard.title != 'changed title'

    def test_update_no_auth(self, tclient, fboard):
        resp = tclient.post('/users/login', data=user_schema.dumps(fboard.user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200


        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % fboard.id, data=board_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 401
        assert result['errors']['message'] == 'Can\'t update.'
        assert fboard.title != 'changed title'


class TestDeleteBoard:
    def test_delete_board(self, tclient, fboard):
        resp = tclient.post('/users/login', data=user_schema.dumps(fboard.user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200

        # board delete
        resp = tclient.delete('/boards/%d' % fboard.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 200
        assert fboard.status == BoardStatus.DELETED
        assert Board.query.filter(Board.status!=2).count() == 9

    def test_delete_no_login(self, tclient, fboard):
        resp = tclient.delete('/boards/%d' % fboard.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 400
        assert result['errors']['message'] == 'Login First.'
        assert fboard.status != 2

    def test_delete_no_auth(self, tclient, fboard):
        resp = tclient.post('/users/login', data=user_schema.dumps(fboard.user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200

        resp = tclient.delete('/boards/%d' % fboard.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 401
        assert result['errors']['message'] == 'Can\'t delete.'
        assert fboard.status == 0
        assert Board.query.filter(Board.status != 2).count() == 10
