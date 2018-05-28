import pytest
from parker_board.model.board import Board
from flask import session
from parker_board.service import board_service
from tests.factories.user import FakeUserFactory
from tests.factories.board import FakeBoardFactory



@pytest.fixture
def board(client):
    user = FakeUserFactory()
    board = FakeBoardFactory(user_id=user.id)

    yield board



# def test_add_board(client):
#     user = FakeUserFactory.create()
#
#     session['current_user'] = user
#
#     board_data = {'title':'helloworld', 'description':'helloworld description'}
#
#     resp = client.post('/boards', data=board_data)
#     assert resp is None

def test_update_board(client):
    user = FakeUserFactory()
    board = FakeBoardFactory(user_id=user.id)

    assert board is not None

    resp = client.patch('/boards/3', data={ 'title':'testing!!!', 'description':'funcing!!!!'})
    print(resp.get_json())
    assert False
