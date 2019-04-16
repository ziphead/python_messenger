import pytest
from routes import resolve


@pytest.fixture
def controller():
    return lambda arg: arg


@pytest.fixture
def routes(controller):
    return [
        {'action': 'echo', 'controller': controller},
    ]


def test_resolve(routes, controller):
    resolved = resolve('echo', routes)
    assert resolved == controller
