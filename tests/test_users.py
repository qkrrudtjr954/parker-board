import pytest
import json
from tests.factories.user import FakeUserFactory
from app.schema.user import before_login_schema, before_register_schema
from app.model.user import User, UserStatus
from marshmallow import ValidationError


class Describe_UserController:
    class Describe_login:
        @pytest.fixture
        def user(self):
            user = FakeUserFactory()
            self.session.flush()
            return user

        @pytest.fixture
        def login_data(self, user):
            return before_login_schema.dumps(user).data

        @pytest.fixture
        def subject(self, login_data):
            resp = self.client.post('/users/login', data=login_data, content_type='application/json')
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        class Context_password가_틀렸을_때:
            @pytest.fixture
            def login_data(self, user):
                user.password = 'incorrect_password'
                return before_login_schema.dumps(user).data

            def test_400을_반환한다(self, subject):
                assert 400 == subject.status_code

        class Context_email이_틀렸을_때:
            @pytest.fixture
            def login_data(self, user):
                user.email = 'incorrect@email.com'
                return before_login_schema.dumps(user).data

            def test_400을_반환한다(self, subject):
                assert 400 == subject.status_code

        @pytest.mark.parametrize('email', ['', None])
        class Context_email이_없을_때:
            @pytest.fixture
            def user(self, email):
                user = FakeUserFactory(email=email)
                self.session.flush()
                return user

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('password', ['', None])
        class Context_password가_없을_때:
            @pytest.fixture
            def user(self, password):
                user = FakeUserFactory(password=password)
                self.session.flush()
                return user

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('email', ['asdf@asdf', 'sample.sample.com', 'sample@sample'])
        class Context_email구조가_아닐_때:
            @pytest.fixture
            def user(self, email):
                user = FakeUserFactory(email=email)
                self.session.flush()
                return user

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('password', ['asdf', 'shorpwd', 'seven!!'])
        class Context_password가_짧을_때:
            @pytest.fixture
            def user(self, password):
                user = FakeUserFactory(password=password)
                self.session.flush()
                return user

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code




@pytest.fixture(scope='function')
def fuser(tsession):
    return FakeUserFactory.build()


@pytest.fixture(scope='function')
def no_email_user(tsession):
    return FakeUserFactory.build(email='')


@pytest.fixture(scope='function')
def no_password_user(tsession):
    return FakeUserFactory.build(password='')


@pytest.fixture(scope='function')
def not_email_user(tsession):
    return FakeUserFactory.build(email='asdfasdf.com')


@pytest.fixture(scope='function')
def short_password_user(tsession):
    return FakeUserFactory.build(password='asdf')


class TestRegister():
    def test_no_email(self, tclient, no_email_user):
        with pytest.raises(ValidationError):
            resp = tclient.post('/users', data=before_register_schema.dumps(no_email_user).data, content_type='application/json')
            assert resp.statud_code == 422

    def test_no_password(self, tclient, no_password_user):
        resp = tclient.post('/users/', data=before_register_schema.dumps(no_password_user).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 422
        assert result['errors']['password'] == ['Password too short']

    def test_register(self, tclient, fuser):
        resp = tclient.post('/users/', data=before_register_schema.dumps(fuser).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['email'] == fuser.email

        resp = tclient.post('/users/', data=before_register_schema.dumps(fuser).data, content_type='application/json')

        assert resp.status_code == 400
        assert resp.data == b'That Email already exists.'


@pytest.fixture(scope='function')
def created_user(tsession):
    fake_user = FakeUserFactory()
    tsession.flush()

    return fake_user


@pytest.fixture(scope='function')
def leaved_user(tsession):
    leaved_user = FakeUserFactory(status=UserStatus.INACTIVE)
    tsession.flush()

    return leaved_user


class TestLogin():
    def test_no_email(self, tclient, no_email_user):
        with pytest.raises(ValidationError):
            resp = tclient.post('/users/login', data=before_login_schema.dumps(no_email_user).data, content_type='application/json')
            assert resp.status_code == 422

    def test_no_password(self, tclient, no_password_user):
        resp = tclient.post('/users/login', data=before_login_schema.dumps(no_password_user).data, content_type='application/json')
        assert resp.status_code == 422

    def test_not_email(self, tclient, not_email_user):
        with pytest.raises(ValidationError):
            resp = tclient.post('/users/login', data=before_login_schema.dumps(not_email_user).data, content_type='application/json')
            assert resp.status_code == 422

    def test_short_password(self, tclient, short_password_user):
        resp = tclient.post('/users/login', data=before_login_schema.dumps(short_password_user).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 422
        assert result['errors']['password'] == ['Password too short']

    def test_login(self, tclient, created_user, tsession):
        assert tsession.query(User).one()

        resp = tclient.post('/users/login', data=before_login_schema.dumps(created_user).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['user']['email'] == created_user.email

    def test_leaved_user_login(self, tclient, leaved_user, tsession):
        assert tsession.query(User).one()

        resp = tclient.post('/users/login', data=before_login_schema.dumps(leaved_user).data, content_type='application/json')

        assert resp.status_code == 400
        assert resp.data == b'Leaved User.'

    def test_no_user_login(self, tclient, fuser):
        resp = tclient.post('/users/login', data=before_login_schema.dumps(fuser).data, content_type='application/json')

        assert resp.status_code == 400
        assert resp.data == b'No User.'


class TestLeave():
    def test_leave(self, tclient, created_user):
        resp = tclient.delete('/users/')
        result = json.loads(resp.data)

        assert resp.status_code == 400
        assert result['message'] == 'Login First.'

        resp = tclient.post('/users/login', data=before_login_schema.dumps(created_user).data, content_type='application/json')
        assert resp.status_code == 200

        resp = tclient.delete('/users/')

        assert resp.status_code == 200
        assert not created_user.is_active()




