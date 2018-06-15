from tests.factories.board import FakeBoardFactory
from app.model.board import Board, BoardStatus
from app.schema.board import board_create_form_schema, board_update_form_schema
from app.schema.user import before_login_schema
from app.model.user import User
import pytest
import json

from tests.factories.post import FakePostFactory
from tests.factories.user import FakeUserFactory


@pytest.fixture(scope='function')
def fboard_build():
    board = FakeBoardFactory.build()
    return board


@pytest.fixture(scope='function')
def no_title_fboard_build():
    board = FakeBoardFactory.build(title=None)
    return board


@pytest.fixture(scope='function')
def fboard(tsession):
    board = FakeBoardFactory()
    tsession.flush()
    return board


@pytest.fixture(scope='function')
def fboards(tsession):
    board = FakeBoardFactory.create_batch(10)
    tsession.flush()
    return board


@pytest.fixture(scope='function')
def many_post_board(tsession):
    board = FakeBoardFactory()
    tsession.flush()

    for i in range(15):
        FakePostFactory(board=board, board_id=board.id)
    tsession.flush()
    return board



class Describe_BoardController:
    class Describe_main:
        @pytest.fixture
        def boards(self):
            boards = FakeBoardFactory.create_batch(25)
            self.session.flush()

            return boards


        @pytest.fixture
        def json_result(self, subject):
            return json.loads(subject.data)

        class Context_per_page가_있을_때:
            @pytest.fixture
            def subject(self, boards, pagination):
                resp = self.client.get('/boards/?per_page=%d&page=%d' % (pagination['per_page'], pagination['page']))
                return resp

            @pytest.fixture
            def pagination(self):
                return dict(per_page=5, page=1)

            def test_200을_반환한다(self, subject):
                assert 200 == subject.status_code

            class Context_page가_1일_때:
                def test_has_prev는_False다(self, json_result):
                    assert not json_result['pagination']['has_prev']

                def test_has_next는_True다(self, json_result):
                    assert json_result['pagination']['has_next']

            class Context_page가_5일_때:
                @pytest.fixture
                def pagination(self):
                    return dict(per_page=5, page=5)
                def test_has_next는_False다(self, json_result):
                    assert not json_result['pagination']['has_next']

                def test_has_prev는_True다(self, json_result):
                    assert json_result['pagination']['has_prev']

        # class Context_page가_없을_때:
        #     @pytest.fixture
        #     def subject(self, boards):
        #         resp = self.client.get('/boards/')
        #         return resp
        #
        #     def test_per_page는_10이다(self, json_result):
        #         result = json.loads(json_result.data)
        #         assert 10 == result['pagination']['page']
        #
        # class Context_per_page가_5일때:
        #     class Context_page가_없을_때:
        #         pass
        #     class Context_page가_5일_때:
        #         pass

    class Describe_create:
        @pytest.fixture
        def form(self):
            board = FakeBoardFactory.build()
            return board_create_form_schema.dump(board).data

        @pytest.fixture
        def subject(self, user, form):
            return self.client.post('/boards', data=json.dumps(form), content_type='application/json')

        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

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
                user = FakeUserFactory.create()
                self.session.flush()
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
            board = FakeBoardFactory(user=user, user_id=user.id)
            self.session.flush()

            return board.id

        @pytest.fixture
        def user(self):
            user = FakeUserFactory()
            self.session.flush()

            resp = self.client.post('/users/login', data=before_login_schema.dumps(user).data, content_type='application/json')
            assert resp.status_code == 200

            return user

        @pytest.fixture
        def subject(self, board_id, update_data):
            resp = self.client.patch('/boards/%d' % board_id, data=update_data, content_type='application/json')
            return resp


        class Context_로그인이_되어있지_않은_경우:
            @pytest.fixture
            def user(self):
                user = FakeUserFactory.create()
                self.session.flush()

                return user

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_board가_존재하지_않을_경우:
            @pytest.fixture
            def board_id(self, user):
                board = FakeBoardFactory.build(user=user, user_id=user.id)
                return board.id

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

        class Context_본인_게시글이_아닌_경우:
            @pytest.fixture
            def board_id(self):
                board = FakeBoardFactory()
                self.session.flush()

                return board.id

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_본인_게시글인_경우:

            def test_200을_반환한다(self, subject):
                assert 200 == subject.status_code

            def test_board가_갱신된다(self, subject, board_id):
                result = json.loads(subject.data)

                db_board = Board.query.get(board_id)

                assert result['id'] == board_id
                assert db_board.title == 'changed title'
                assert db_board.description == 'changed description'

        @pytest.mark.parametrize('title', ['', None])
        class Context_title이_없는_경우:
            @pytest.fixture
            def update_data(self, title):
                update_data = dict(title=title, description='changed description')
                return board_update_form_schema.dumps(update_data).data

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

    class Describe_delete:
        class Context_로그인이_되어있는_경우:
            @pytest.fixture
            def user(self):
                user = FakeUserFactory()
                self.session.flush()
                resp = self.client.post('/users/login', data=before_login_schema.dumps(user).data, content_type='application/json')
                assert 200 == resp.status_code
                return user

            @pytest.fixture
            def subject(self, board_id):
                resp = self.client.delete('/boards/%d' % board_id)
                return resp

            class Context_board가_없는_경우:
                @pytest.fixture
                def board_id(self, user):
                    board = FakeBoardFactory(user=user, user_id=user.id)
                    return board.id

                def test_404를_반환한다(self, subject):
                    assert 404 == subject.status_code

            class Context_board가_있는_경우:
                class Context_본인_board_경우:
                    @pytest.fixture
                    def board_id(self, user):
                        board = FakeBoardFactory(user=user, user_id=user.id)
                        self.session.flush()
                        return board.id

                    def test_204를_반환한다(self, subject):
                        assert 204 == subject.status_code

                    def test_board를_삭제한다(self, subject, board_id):
                        db_board = Board.query.filter_by(id=board_id).one()
                        assert db_board.is_deleted()

                class Context_본인_board가_아닌_경우:
                    @pytest.fixture
                    def board_id(self, user):
                        board = FakeBoardFactory()
                        self.session.flush()
                        return board.id

                    def test_401을_반환한다(self, board_id):
                        resp = self.client.delete('/boards/%d' % board_id)
                        assert 401 == resp.status_code

        class Context_로그인이_되어있지_않은_경우:
            @pytest.fixture
            def board_id(self):
                board = FakeBoardFactory()
                self.session.flush()

                return board.id

            def test_401을_반환한다(self, board_id):
                resp = self.client.delete('/boards/%d' % board_id)
                assert 401 == resp.status_code




class TestCreateBoard:
    def test_create_board(self, tclient, tsession, fboard_build):
        login_user = fboard_build.user

        tsession.add(login_user)
        tsession.flush()

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')
        assert resp.status_code == 200

        resp = tclient.post('/boards', data=board_create_form_schema.dumps(fboard_build).data, content_type='application/json')
        result = json.loads(resp.data)
        assert resp.status_code == 200

        board_id = result['id']
        board = Board.query.get(board_id)
        assert fboard_build.user.id == board.user.id
        assert fboard_build.title == board.title

    def test_no_title_create_board(self, tclient, tsession, no_title_fboard_build):
        login_user = no_title_fboard_build.user

        tsession.add(login_user)
        tsession.flush()

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')
        assert resp.status_code == 200

        resp = tclient.post('/boards', data=board_create_form_schema.dumps(no_title_fboard_build).data, content_type='application/json')

        assert resp.status_code == 422


class TestBoardList:
    def test_board_list(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        resp = tclient.get('/boards/')

        assert resp.status_code == 200

        result = json.loads(resp.data)

        assert len(result['boards']) == 10
        assert result['boards'][0]['user']['email'] == fboards[0].user.email

    def test_board_list_페이지_3개(self, tclient, fboards):
        assert len(fboards) == 10
        assert Board.query.count() == 10
        assert User.query.count() == 10

        resp = tclient.get('/boards/?per_page=3')

        assert resp.status_code == 200

        result = json.loads(resp.data)

        assert len(result['boards']) == 3

    def test_read_board(self, tclient, many_post_board):

        login_user = many_post_board.user

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')
        assert resp.status_code == 200

        resp = tclient.get('/boards/%d/posts' % many_post_board.id)
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert len(result['posts']) == 10

        resp = tclient.get('/boards/%d/posts?per_page=5' % many_post_board.id)
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert len(result['posts']) == 5
        assert result['pagination']['has_next']
        assert not result['pagination']['has_prev']

        resp = tclient.get('/boards/%d/posts?per_page=15' % many_post_board.id)
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert not result['pagination']['has_next']
        assert not result['pagination']['has_prev']


class TestUpdateBoard:
    def test_update_board(self, tclient, fboard, tsession):
        assert tsession.query(User).one()
        assert tsession.query(Board).one()

        data = before_login_schema.dumps(fboard.user).data
        resp = tclient.post('/users/login', data=data, content_type='application/json')
        assert resp.status_code == 200

        # board update
        board = fboard
        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % board.id, data=board_update_form_schema.dumps(update_data).data, content_type='application/json')

        assert resp.status_code == 200
        assert board.title == 'changed title'

    def test_update_no_login(self, tclient, fboard):
        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % fboard.id, data=board_update_form_schema.dumps(update_data).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 401
        assert result['message'] == 'Login First.'
        assert fboard.title != 'changed title'

    def test_update_no_auth(self, tclient, fboards):
        login_user = fboards[0].user

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')
        assert resp.status_code == 200

        update_board = fboards[1]

        update_data = dict(title='changed title')
        resp = tclient.patch('/boards/%d' % update_board.id, data=board_update_form_schema.dumps(update_data).data, content_type='application/json')

        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'
        assert update_board.title != 'changed title'


class TestDeleteBoard:
    def test_delete_board(self, tclient, fboard):
        resp = tclient.post('/users/login', data=before_login_schema.dumps(fboard.user).data, content_type='application/json')
        assert resp.status_code == 200

        # board delete
        resp = tclient.delete('/boards/%d' % fboard.id, content_type='application/json')

        assert resp.status_code == 204
        assert fboard.is_deleted()

    def test_delete_no_login(self, tclient, fboard):
        resp = tclient.delete('/boards/%d' % fboard.id, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 401
        assert result['message'] == 'Login First.'
        assert fboard.title != 'changed title'

    def test_delete_no_auth(self, tclient, fboards):
        login_user = fboards[0].user

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')
        assert resp.status_code == 200

        delete_board = fboards[1]
        resp = tclient.delete('/boards/%d' % delete_board.id, content_type='application/json')

        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'
        assert not delete_board.is_deleted()
