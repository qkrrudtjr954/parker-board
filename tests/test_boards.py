import pytest
import json

from app.model.board import Board
from app.schema.board import board_create_form_schema, board_update_form_schema

from tests.factories.user import UserFactory
from tests.factories.board import BoardFactory


class Describe_BoardController:
    class Describe_get_board:
        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

        @pytest.fixture
        def board_id(self, user):
            board = BoardFactory(user_id=user.id, user=user)
            self.session.commit()
            return board.id

        @pytest.fixture
        def subject(self, board_id):
            resp = self.client.get('/boards/%d' % board_id)
            return resp

        @pytest.fixture
        def json_result(self, subject):
            return json.loads(subject.data)

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        class Context_Board가_없을_때:
            @pytest.fixture
            def board_id(self, user):
                board = BoardFactory.build(user_id=user.id, user=user)
                return board.id

            def test_404를_반환하다(self, subject):
                assert 404 == subject.status_code

    class Describe_main:
        @pytest.fixture
        def boards(self):
            boards = BoardFactory.create_batch(25)
            return boards

        @pytest.fixture
        def subject(self, boards):
            resp = self.client.get('/boards')
            return resp

        @pytest.fixture
        def json_result(self, subject):
            return json.loads(subject.data)

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_Board의_길이는_25이다(self, json_result):
            assert 25 == len(json_result)

    class Describe_create:
        @pytest.fixture
        def form(self):
            board = BoardFactory.build()
            return board_create_form_schema.dump(board).data

        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

        @pytest.fixture
        def subject(self, user, form):
            return self.client.post('/boards', data=json.dumps(form), content_type='application/json')

        def test_200이_반환된다(self, subject):
            assert 200 == subject.status_code

        def test_board가_생성된다(self, subject, logged_in_user, form):
            result = json.loads(subject.data)
            board_id = result['id']

            db_board = Board.query.get(board_id)
            assert logged_in_user.id == db_board.user_id
            assert form['title'] == db_board.title

        @pytest.mark.parametrize("title", ['', None])
        class Context_title이_없는경우:
            @pytest.fixture
            def form(self, form, title):
                form['title'] = title
                return form

            def test_422가_반환된다(self, subject):
                assert 422 == subject.status_code

        class Context_로그인이_되어있지_않은경우:
            @pytest.fixture
            def user(self):
                user = UserFactory.create()
                self.session.commit()
                return user

            def test_401이_반환된다(self, subject):
                assert 401 == subject.status_code

    class Describe_update:
        @pytest.fixture
        def update_data(self):
            update_data = dict(title='changed title', description='changed description')
            return board_update_form_schema.dumps(update_data).data

        @pytest.fixture
        def board_id(self, user):
            board = BoardFactory(user=user, user_id=user.id)
            self.session.commit()

            return board.id

        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

        @pytest.fixture
        def subject(self, board_id, update_data):
            resp = self.client.patch('/boards/%d' % board_id, data=update_data, content_type='application/json')
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_board가_갱신된다(self, subject, board_id):
            result = json.loads(subject.data)

            db_board = Board.query.get(board_id)

            assert result['id'] == board_id
            assert db_board.title == 'changed title'
            assert db_board.description == 'changed description'

        class Context_로그인이_되어있지_않은_경우:
            @pytest.fixture
            def user(self):
                user = UserFactory.create()
                self.session.commit()

                return user

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_board가_존재하지_않을_경우:
            @pytest.fixture
            def board_id(self, user):
                board = BoardFactory.build(user=user, user_id=user.id)
                return board.id

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

        class Context_본인_게시글이_아닌_경우:
            @pytest.fixture
            def board_id(self):
                board = BoardFactory()
                self.session.commit()

                return board.id

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        @pytest.mark.parametrize('title', ['', None])
        class Context_title이_없는_경우:
            @pytest.fixture
            def update_data(self, title):
                update_data = dict(title=title, description='changed description')
                return board_update_form_schema.dumps(update_data).data

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

    class Describe_delete:
        @pytest.fixture
        def subject(self, board_id):
            resp = self.client.delete('/boards/%d' % board_id)
            return resp

        @pytest.fixture
        def board_id(self, user):
            board = BoardFactory(user=user, user_id=user.id)
            self.session.commit()
            return board.id

        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

        def test_204를_반환한다(self, subject):
            assert 204 == subject.status_code

        def test_board를_삭제한다(self, subject, board_id):
            db_board = Board.query.filter_by(id=board_id).one()
            assert db_board.is_deleted

        class Context_board가_없는_경우:
            @pytest.fixture
            def board_id(self, user):
                board = BoardFactory.build(user=user, user_id=user.id)
                return board.id

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

        class Context_본인_board가_아닌_경우:
            @pytest.fixture
            def board_id(self, user):
                board = BoardFactory()
                self.session.commit()
                return board.id

            def test_401을_반환한다(self, board_id):
                resp = self.client.delete('/boards/%d' % board_id)
                assert 401 == resp.status_code

        class Context_로그인이_되어있지_않은_경우:
            @pytest.fixture
            def user(self):
                user = UserFactory()
                self.session.commit()

                return user

            def test_401을_반환한다(self, board_id):
                resp = self.client.delete('/boards/%d' % board_id)
                assert 401 == resp.status_code

