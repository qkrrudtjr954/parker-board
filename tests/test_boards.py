from tests.factories.board import FakeBoardFactory, FakeBoardAndUserFactory
from tests.factories.user import FakeUserFactory
from parker_board.model.board import Board
from parker_board.schema.board import board_schema
from parker_board.schema.resp import resp_schema
from parker_board.schema.user import login_schema
from parker_board.model.user import User
from flask_login import current_user
import pytest



@pytest.fixture(scope='function')
def fuser(tclient, tsession):
    user = FakeUserFactory()
    tsession.add(user)
    tsession.flush()

    resp = tclient.post('/users/login', data=login_schema.dumps(user).data, content_type='application/json')
    result = resp_schema.loads(resp.data.decode()).data

    assert result['status_code'] == 200

    yield user


@pytest.fixture(scope='function')
def fboards(tsession):
    board = FakeBoardAndUserFactory.create_batch(10)
    tsession.flush()
    return board


class TestBoard:
    # def test_create_board(self, tclient, fuser):
    #     resp = tclient.post('/boards', data=board_schema.dumps(fboard).data, content_type='application/json')
    #     result = resp_schema.loads(resp.data.decode()).data
    #     assert result['status_code'] == 200


    def test_read_board(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        resp = tclient.get('/')
        result = resp_schema.loads(resp.data.decode()).data

        assert len(result['data']['boards']) == 3

    def test_update_board(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        # login
        login_user = fboards[0].user

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200

        # board update
        board = fboards[0]
        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % board.id, data=board_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 200
        assert Board.query.get(board.id).title == 'changed title'

    def test_delete_board(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        # login
        login_user = fboards[0].user

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200

        # board delete
        board = fboards[0]
        resp = tclient.delete('/boards/%d' % board.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 200
        assert board.status == 2
        assert Board.query.filter(Board.status!=2).count() == 9

    def test_delete_no_auth(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        # login
        login_user = fboards[1].user

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200

        # board delete
        board = fboards[0]

        assert board.user != login_user

        resp = tclient.delete('/boards/%d' % board.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 401
        assert result['errors']['error'] == 'Can\'t delete.'
        assert board.status == 0
        assert Board.query.filter(Board.status != 2).count() == 10
