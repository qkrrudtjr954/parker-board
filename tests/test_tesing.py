import pytest


# using Context
class Describe_UsingContext:
    class Describe_Something:
        class Context_when_logged_in:
            def test_is_expected_200(self):
                pass
        class Context_when_not_logged_in:
            def test_is_expected_400(self):
                pass




class Describe_NotUsingContext2:
    class Describe_Something:
        class Context_when_logged_in:
            def test_is_expected_200_when_user_has_some_status(self):
                pass


class Describe_Using_Long_Context:
    class Context_when_describe_to_long:
        class Describe_Using_Context2:
            def test_using_context(self):
                print('using context test')
                pass

            class Context_when_user_has_some_status:
                def test_is_expected_200(self):
                    pass


class Hero(object):
    def __init__(self, sword):
        self.sword = sword

    def has_sword(self):
        return True if self.sword is not None else False


@pytest.fixture
def double_sword_hero():
    return Hero('double')


@pytest.fixture
def single_sword_hero():
    return Hero('single')


@pytest.fixture
def no_sword_hero():
    return Hero(None)




class Describe_hero_sword:
    class Context_when_hero_has_sword:
        class Test_sword_is_double:
            def test_is_hero_has_sword(self, single_sword_hero):
                assert single_sword_hero.has_sword

            def test_is_double_sword(self, double_sword_hero):
                assert double_sword_hero.sword == 'double'

        class Test_sword_id_single:
            def test_is_hero_has_sword(self, single_sword_hero):
                assert single_sword_hero.has_sword

            def test_is_double_sword(self, single_sword_hero):
                assert single_sword_hero.sword == 'single'

    class Context_when_hero_has_not_sword:
        def test_is_expected_to_fail(self, no_sword_hero):
            assert no_sword_hero.sword is None


@pytest.fixture
def hero():
    return Hero('double')


@pytest.fixture
def hero_type(hero):
    return type(hero)


class Describe_Hero_type:
    def test_hero_type(self, hero, hero_type):
        assert type(hero) is hero_type