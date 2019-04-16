import pytest
from datetime import datetime
from protocol import make_response


@pytest.fixture
def success_status():
    return 201


@pytest.fixture
def valid_request():
    return {
        'action': 'upper_text',
        'time': datetime.now().timestamp()
    }


@pytest.fixture
def assert_response(success_status):
    return {
        'action': 'upper_text',
        'user': None,
        'time': datetime.now().timestamp(),
        'data': None,
        'code': success_status,
    }


def test_make_response(
    valid_request,
    assert_response,
    success_status
):
    response = make_response(
        valid_request,
        success_status,
    )

    assert response.get('action') == assert_response.get('action')
    assert response.get('user') == assert_response.get('user')
    assert response.get('data') == assert_response.get('data')
    assert response.get('code') == assert_response.get('code')
