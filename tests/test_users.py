import pytest
from tests.factories.user import FakeUserFactory
from app.schema.resp import resp_schema
from app.schema.user import login_schema
from app.model.user import User
from marshmallow import ValidationError


@pytest.fixture(scope='function')
def fuser(tsession):
    return FakeUserFactory.build()


@pytest.fixture(scope='function')
def no_email_user(tsession):
    return FakeUserFactory.build(email='')


@pytest.fixture(scope='function')
def no_password_user(tsession):
    return FakeUserFactory.build(password='')


class TestRegister():
    def test_no_email(self, tclient, no_email_user):
        with pytest.raises(ValidationError):
            resp = tclient.post('/users', data=login_schema.dumps(no_email_user).data, content_type='application/json')
            result = resp_schema.loads(resp.data.decode()).data

    def test_no_password(self, tclient, no_password_user):
        resp = tclient.post('/users', data=login_schema.dumps(no_password_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 422

    def test_register(self, tclient, fuser):
        resp = tclient.post('/users', data=login_schema.dumps(fuser).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 200
        assert result['data']['email'] == fuser.email

        resp = tclient.post('/users', data=login_schema.dumps(fuser).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 400
        assert result['errors']['message'] == 'Duplicate Email.'


@pytest.fixture(scope='function')
def dummy_register(tsession, fuser):
    tsession.add(fuser)
    tsession.flush()
    yield fuser


@pytest.fixture(scope='function')
def dummy_leaved_user(tsession, fuser):
    fuser.status = 2
    tsession.add(fuser)
    tsession.flush()
    yield fuser


class TestLogin():
    def test_no_email(self, tclient, no_email_user):
        with pytest.raises(ValidationError):
            resp = tclient.post('/users/login', data=login_schema.dumps(no_email_user).data, content_type='application/json')
            result = resp_schema.loads(resp.data.decode()).data
            assert result['status_code'] == 422

    def test_no_password(self, tclient, no_password_user):
        resp = tclient.post('/users/login', data=login_schema.dumps(no_password_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 422

    def test_login(self, tclient, dummy_register, tsession):
        assert tsession.query(User).one()

        resp = tclient.post('/users/login', data=login_schema.dumps(dummy_register).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200

    def test_leaved_user_login(self, tclient, dummy_leaved_user, tsession):
        assert tsession.query(User).one()

        resp = tclient.post('/users/login', data=login_schema.dumps(dummy_leaved_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 401
        assert result['errors']['message'] == 'Leaved User.'

    def test_no_user_login(self, tclient, fuser):
        resp = tclient.post('/users/login', data=login_schema.dumps(fuser).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 400
        assert result['errors']['message'] == 'No User.'


class TestLeave():
    def test_leave(self, tclient, dummy_register):
        resp = tclient.delete('/users/%d' % dummy_register.id, data=login_schema.dumps(dummy_register).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 400
        assert result['errors']['message'] == 'Login First.'

        resp = tclient.post('/users/login', data=login_schema.dumps(dummy_register).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200

        resp = tclient.delete('/users/%d' % dummy_register.id, data=login_schema.dumps(dummy_register).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert result['status_code'] == 200
        assert result['data']['user']['status'] == 2

