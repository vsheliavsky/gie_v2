# pyright: basic
from enum import Enum
from unittest.mock import MagicMock

import pytest
import requests

from src.clients.gie_client import GieClient


class TestApiType(Enum):
    AGSI = "https://agsitest.gie.eu/api/"
    ALSI = "https://alsitest.gie.eu/api/"


@pytest.fixture
def valid_api_key():
    return "valid_api_key"


@pytest.fixture
def wrong_api_key():
    return "wrong_api_key"


@pytest.fixture
def mock_session():
    session = MagicMock(spec=requests.Session)
    session.headers = dict()
    return session


@pytest.fixture
def gie_client(mock_session, valid_api_key):
    """Fixture to create a GieClient instance with a mock session."""
    mock_session.headers["x-key"] = valid_api_key
    return GieClient(api_key=valid_api_key, session=mock_session)


def test_valid_session(mock_session, valid_api_key):
    mock_session.headers["x-key"] = valid_api_key
    client = GieClient(api_key=valid_api_key, session=mock_session)

    assert client.session.headers["x-key"] == valid_api_key
    assert client.api_key == valid_api_key


def test_missing_header(mock_session, valid_api_key):
    with pytest.raises(
        ValueError, match="Session headers must include 'x-key'"
    ):
        GieClient(api_key=valid_api_key, session=mock_session)


def test_incorrect_header(mock_session, valid_api_key, wrong_api_key):
    session = mock_session
    session.headers["x-key"] = wrong_api_key
    with pytest.raises(
        ValueError, match="Session headers include incorrect 'x-key'"
    ):
        GieClient(api_key=valid_api_key, session=session)


def test_fetch_success(gie_client, mock_session):
    """Test fetch with a successful response."""
    # Setup params
    api_type = TestApiType.AGSI
    params = {"param1": "value1"}
    endpoint = "test_endpoint"

    # Setup mock session and response
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "success"}
    mock_session.get.return_value = mock_response

    # Set expected outcomes
    expected_url = "https://agsitest.gie.eu/api/test_endpoint"
    expected_params = {"param1": "value1"}

    # Call function
    result = gie_client.fetch(
        api_type=api_type, params=params, endpoint=endpoint
    )

    # Verify the request URL and parameters
    mock_session.get.assert_called_once_with(
        url=expected_url, params=expected_params
    )

    # Verify the response
    assert result == {"result": "success"}
