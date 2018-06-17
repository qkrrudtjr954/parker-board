import pytest
import json
from tests.factories.user import FakeUserFactory
from app.schema.user import before_login_schema, before_register_schema
from app.model.user import User


class Describe_UserController:
    @pytest.fixture
    def json_result(self, subject):
        return json.loads(subject.data)

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
            def login_data(self, user, email):
                user.email = email
                return before_login_schema.dumps(user).data

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('password', ['', None])
        class Context_password가_없을_때:
            @pytest.fixture
            def login_data(self, user, password):
                user.password = password
                return before_login_schema.dumps(user).data

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

    class Describe_register:
        @pytest.fixture
        def form(self):
            user = FakeUserFactory.build()
            return user

        @pytest.fixture
        def subject(self, form):
            resp = self.client.post('/users/', data=before_register_schema.dumps(form).data, content_type='application/json')
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_user가_DB에_저장된다(self, form, json_result):
            user_id = json_result['id']

            db_user = User.query.get(user_id)

            assert db_user.email == form.email
            assert db_user.password == form.password

        class Context_중복_email일_때:
            @pytest.fixture
            def form(self):
                user = FakeUserFactory()
                self.session.flush()
                return user

            def test_400을_반환한다(self, subject):
                assert 400 == subject.status_code

        @pytest.mark.parametrize('email', ['', None])
        class Context_email이_없을_때:
            @pytest.fixture
            def form(self, email):
                user = FakeUserFactory.build(email=email)
                return user

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('password', ['', None])
        class Context_password가_없을_때:
            @pytest.fixture
            def form(self, password):
                user = FakeUserFactory.build(password=password)
                return user

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('email', ['asdf@asdf', 'sample.sample.com', 'sample@sample'])
        class Context_email구조가_아닐_때:
            @pytest.fixture
            def form(self, email):
                user = FakeUserFactory.build(email=email)
                return user

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('password', ['asdf', 'shorpwd', 'seven!!'])
        class Context_password가_짧을_때:
            @pytest.fixture
            def form(self, password):
                user = FakeUserFactory.build(password=password)
                return user

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

    class Describe_leave:
        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

        @pytest.fixture
        def subject(self, user):
            resp = self.client.delete('/users/')
            return resp

        def test_204를_반환한다(self, subject):
            assert 204 == subject.status_code

        def test_user의_상태가_변경된다(self, subject, user):
            assert not user.is_active()

        class Context_로그인하지_않았을_때:
            @pytest.fixture
            def user(self, not_logged_in_user):
                return not_logged_in_user

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code
