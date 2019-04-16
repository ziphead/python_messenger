import pytest
from datetime import datetime
from protocol import validate_request


@pytest.fixture
def valid_request():
    return {
        'action': 'upper_text',
        'time': datetime.now().timestamp()
    }


@pytest.fixture
def invalid_request():
    return {}


def test_validate_request_success(
    valid_request
):
    assert validate_request(valid_request) == True


def test_validate_request_fail(
    invalid_request
):
    assert validate_request(invalid_request) == False
