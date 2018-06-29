import pytest
import json

from app.model.like import Like
from app.model.post import Post
from app.schema.post import post_create_form_schema, post_update_form_schema
from tests.factories.like import FakeLikeFactory

from tests.factories.post import FakePostFactory
from tests.factories.board import FakeBoardFactory


class Describe_PostController:
    @pytest.fixture
    def user(self, logged_in_user):
        return logged_in_user

    @pytest.fixture
    def pagination(self):
        return dict(per_page=10, page=1)

    @pytest.fixture
    def json_result(self, subject):
        return json.loads(subject.data)

    @pytest.fixture
    def param(self, pagination):
        param = '?'
        if 'per_page' in pagination:
            param += 'per_page=%d&' % pagination['per_page']
        if 'page' in pagination:
            param += 'page=%d' % pagination['page']
        return param

    class Describe_post_list:

        @pytest.fixture
        def board(self):
            board = FakeBoardFactory()
            board.posts = FakePostFactory.create_batch(20)
            self.session.commit()

            return board

        @pytest.fixture
        def subject(self, user, board, param):
            resp = self.client.get('/boards/%d/posts%s' % (board.id, param))
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code


        class Context_board가_존재하지_않을_때:
            @pytest.fixture
            def board(self):
                board = FakeBoardFactory.build()
                return board

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

        class Context_로그인_하지_않았을_때:
            def test_200을_반환한다(self, subject):
                assert 200 == subject.status_code

    class Describe_detail:
        @pytest.fixture
        def post_id(self):
            post = FakePostFactory()
            return post.id

        @pytest.fixture
        def subject(self, user, post_id):
            resp = self.client.get('/posts/%d' % post_id)
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_DB에서_post를_가져온다(self, post_id, json_result):
            db_post = Post.query.get(post_id)

            assert db_post.title == json_result['title']
            assert db_post.content == json_result['content']

        class Context_post가_존재하지_않을_때:
            @pytest.fixture
            def post_id(self):
                post = FakePostFactory.build()
                return post.id

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

        class Context_로그인_하지_않았을_때:
            @pytest.fixture
            def user(self, not_logged_in_user):
                return not_logged_in_user

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_15개_좋아요를_받았을때:
            @pytest.fixture
            def post_id(self):
                post = FakePostFactory()
                post.likes = FakeLikeFactory.create_batch(15)
                return post.id

            @pytest.fixture
            def json_result(self, subject):
                return json.loads(subject.data)

            def test_post의_like_count는_15이다(self, json_result):
                assert 15 == json_result['like_count']

    class Describe_create:
        @pytest.fixture
        def target_board_id(self):
            board = FakeBoardFactory()
            self.session.commit()

            return board.id

        @pytest.fixture
        def form(self):
            post = FakePostFactory.build()
            return post

        @pytest.fixture
        def subject(self, user, form, target_board_id):
            resp = self.client.post('/boards/%d/posts' % target_board_id, data=post_create_form_schema.dumps(form).data, content_type='application/json')
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_DB에_post를_저장한다(self, user, json_result, form):
            post_id = json_result['id']

            db_post = Post.query.get(post_id)

            assert db_post.title == form.title
            assert db_post.content == form.content
            assert db_post.description == form.description
            assert db_post.user_id == user.id

        @pytest.mark.parametrize('title', ['', None])
        class Context_title이_없을_때:
            @pytest.fixture
            def form(self, title):
                post = FakePostFactory.build(title=title)
                return post

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('content', ['', None])
        class Context_content가_없을_때:
            @pytest.fixture
            def form(self, content):
                post = FakePostFactory.build(content=content)
                return post

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('title', ['helo', 'srt', '짧은제목'])
        class Context_title이_10글자_이하일_때:
            @pytest.fixture
            def form(self, title):
                post = FakePostFactory.build(title=title)
                return post

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('content', ['1234567890123456789', 'very short content', 'smaller than 20'])
        class Context_content가_20글자_이하일_때:
            @pytest.fixture
            def form(self, content):
                post = FakePostFactory.build(content=content)
                return post

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        class Context_로그인을_하지_않았을_때:
            @pytest.fixture
            def user(self, not_logged_in_user):
                return not_logged_in_user


            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

    class Describe_update:
        @pytest.fixture
        def update_data(self):
            return dict(title='changed title', content='this is changed content. and must longer than 20.', description='changed description')

        @pytest.fixture
        def target_post(self, user):
            post = FakePostFactory(user_id=user.id, user=user)
            self.session.commit()
            return post

        @pytest.fixture
        def subject(self, user, update_data, target_post):
            resp = self.client.patch('/posts/%d' % target_post.id, data=post_update_form_schema.dumps(update_data).data, content_type='application/json')
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_DB에_post가_갱신된다(self, json_result, update_data):
            post_id = json_result['id']

            db_post = Post.query.get(post_id)

            assert db_post.id == post_id
            assert db_post.title == update_data['title']
            assert db_post.content == update_data['content']
            assert db_post.description == update_data['description']

        class Context_데이터가_이전과_같을_때:
            @pytest.fixture
            def update_data(self, target_post):
                return dict(title=target_post.title, content=target_post.content, description=target_post.description)

            def test_406을_반환한다(self, subject):
                # 406 혀용되지 않는 요청
                assert 406 == subject.status_code

        class Context_title이_없을_때:
            @pytest.fixture
            def update_data(self):
                return dict(content='this is changed content. and must longer than 20.', description='changed description')

            def test_content_description만_갱신된다(self, json_result, update_data):
                post_id = json_result['id']

                db_post = Post.query.get(post_id)

                assert db_post.id == post_id
                assert db_post.title != ''
                assert db_post.title is not None
                assert db_post.content == update_data['content']
                assert db_post.description == update_data['description']

        class Context_content가_없을_때:
            @pytest.fixture
            def update_data(self):
                return dict(title='changed title', description='changed description')

            def test_title_description만_갱신된다(self, json_result, update_data):
                post_id = json_result['id']

                db_post = Post.query.get(post_id)

                assert db_post.id == post_id
                assert db_post.title == update_data['title']
                assert db_post.content != ''
                assert db_post.content is not None
                assert db_post.description == update_data['description']

        class Context_description이_없을_때:
            @pytest.fixture
            def update_data(self):
                return dict(title='changed title', content='this is changed content. and must longer than 20.')

            def test_title_content만_갱신된다(self, json_result, update_data):
                post_id = json_result['id']

                db_post = Post.query.get(post_id)

                assert db_post.id == post_id
                assert db_post.title == update_data['title']
                assert db_post.content == update_data['content']
                assert db_post.description != ''
                assert db_post.description is not None

        class Context_로그인_하지_않았을_때:
            @pytest.fixture
            def user(self, not_logged_in_user):
                return not_logged_in_user

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

    class Describe_delete:
        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

        @pytest.fixture
        def post_id(self, user):
            post = FakePostFactory(user=user, user_id=user.id)
            self.session.commit()
            return post.id

        @pytest.fixture
        def subject(self, user, post_id):
            resp = self.client.delete('/posts/%d' % post_id)
            return resp

        def test_204를_반환한다(self, subject):
            assert 204 == subject.status_code

        def test_DB에서_상태가_변경된다(self, subject, post_id):
            db_post = Post.query.get(post_id)
            assert db_post.is_deleted

        class Context_post가_존재하지_않는_경우:
            @pytest.fixture
            def post_id(self):
                post = FakePostFactory.build()
                return post.id

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

        class Context_본인_게시글이_아닌_경우:
            @pytest.fixture
            def post_id(self):
                post = FakePostFactory()
                self.session.commit()
                return post.id

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_로그인_하지_않은_경우:
            @pytest.fixture
            def user(self, not_logged_in_user):
                return not_logged_in_user

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

    class Describe_like:
        @pytest.fixture
        def target_post(self):
            post = FakePostFactory()
            return post

        @pytest.fixture
        def subject(self, target_post, user):
            resp = self.client.post('/posts/%d/like' % target_post.id)
            return resp

        def test_200을_반환한다(self, subject):
            return 200 == subject.status_code

        def test_like_table에_좋아요가_추가된다(self, subject, target_post, user):
            assert Like.query.filter(Like.post_id == target_post.id, Like.user_id == user.id).one_or_none()


    class Describe_unlike:
        @pytest.fixture
        def target_post(self, user):
            post = FakePostFactory()
            FakeLikeFactory(post_id=post.id, user_id=user.id)
            print(Like.query.all())
            return post

        @pytest.fixture
        def subject(self, target_post):
            resp = self.client.post('/posts/%d/unlike' % target_post.id)
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_like_table에서_row가_삭제된다(self, subject, target_post, user):
            assert not Like.query.filter(Like.post_id == target_post.id, Like.user_id == user.id).one_or_none()


