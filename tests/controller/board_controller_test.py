import pytest
from parker_board.model.board import Board
from flask import session
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