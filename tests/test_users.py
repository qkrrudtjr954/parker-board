import pytest
from tests.factories.user import FakeUserFactory
from parker_board.schema.user import login_user_schema
from parker_board.schema.resp import resp_schema
from parker_board.model.user import User
from flask_login import login_user, current_user


@pytest.fixture(scope='function')
def fuser(tsession):
    FakeUserFactory._meta.sqlalchemy_session = tsession
    user = FakeUserFactory()
    return user

@pytest.fixture(scope='function')
def fuser_obj(tsession):
    FakeUserFactory._meta.sqlalchemy_session = tsession
    user = FakeUserFactory.build()
    return user


class TestUser:
    def test_sign_in(self, tclient, fuser):
        data = login_user_schema.dumps(fuser).data
        resp = tclient.post('/users/login', data=data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200

    def test_sign_in_wrong_data(self, tclient, fuser):
        # fail case ( wrong password )
        data = login_user_schema.dumps({'email':fuser.email, 'password':'wrong pwd'}).data
        resp = tclient.post('/users/login', data=data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 401

        # fail case ( wrong email )
        data = login_user_schema.dumps({'email': 'fake@fake.com', 'password': fuser.password}).data
        resp = tclient.post('/users/login', data=data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 401

    def test_register(self, tclient, fuser_obj, tsession):
        data = login_user_schema.dumps(fuser_obj).data
        resp = tclient.post('/users', data=data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200
        assert User.query.one()

        User.query.filter(User.id == result['data']['id']).delete()
        tsession.commit()
        assert User.query.count() == 0

    def test_register_no_data(self, tclient, fuser_obj):
        # fail case ( no password )
        data = login_user_schema.dumps({'email': fuser_obj.email}).data
        resp = tclient.post('/users', data=data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 422

    def test_register_wrong_data(self, tclient, fuser_obj):
        # fail case ( not email structure )
        data = login_user_schema.dumps({'email':'fakefake.com', 'password': fuser_obj.password}).data
        resp = tclient.post('/users', data=data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 422

    def test_logout(self, tclient, fuser):
        data = login_user_schema.dumps(fuser).data
        resp = tclient.post('/users/login', data=data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200

        resp = tclient.delete('/users/logout')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200