from tests.factories.board import FakeBoardFactory
from tests.factories.user import FakeUserFactory
from parker_board.model.board import Board
from parker_board.schema.board import board_schema
from parker_board.schema.resp import resp_schema
from flask_login import login_user
import pytest



@pytest.fixture(scope='function')
def fboard(tsession):
    board = FakeBoardFactory.build()
    yield board


class TestBoard:
    def test_board(self, tclient, fboard, tsession):
        resp = tclient.post('/boards', data=board_schema.dump(fboard).data, content_type='application/json')
        result = resp_schema.dumps(resp.data.decode()).data

        assert result['status_code'] == 200
        assert Board.query.one()
