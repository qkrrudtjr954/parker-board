from tests.factories.board import FakeBoardFactory
from tests.factories.user import FakeUserFactory
from parker_board.model.board import Board
from parker_board.schema.board import board_schema
from parker_board.schema.resp import resp_schema
import pytest


@pytest.fixture(scope='function')
def fboard(tsession):
    FakeBoardFactory._meta.sqlalchemy_session = tsession
    board = FakeBoardFactory()

    return board


class TestBoard:
    def test_board(self, tclient, fboard, tsession):
        data = board_schema.dumps(fboard).data
        resp = tclient.post('/boards', data=data, content_type='application/json')
        result = resp_schema.dumps(resp.data.decode()).data

        assert result['status_code'] == 200
        assert Board.query.one()

        Board.query.filter(Board.id == result['data']['id']).delete()
        tsession.flush()

        assert Board.query.count() == 0