# pyright: basic
import datetime
from unittest.mock import MagicMock

import pytest
import requests
from roiti.gie_client.api_models.platform import APIType
from roiti.gie_client.clients.gie_client import GieClient

# ===== Fixture setup =====


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


# ===== Test class instantiation =====


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


# ===== Test fetch =====


def test_fetch_success(gie_client, mock_session):
    """Test fetch with a successful response."""
    # Setup params
    api_type = APIType.AGSI
    params = {"param1": "value1"}
    endpoint = "test_endpoint"

    # Setup mock session and response
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "success"}
    mock_session.get.return_value = mock_response

    # Set expected outcomes
    expected_url = "https://agsi.gie.eu/api/test_endpoint"
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


# ===== Test query_storage =====


def test_query_storage_success(gie_client, mock_session):
    # Mocking the API response and session
    mock_session.get.return_value.json.return_value = {"data": "some data"}
    api_type = APIType.AGSI

    response = gie_client.query_storage(
        api_type=api_type,
        page=1,
        size=30,
        from_date=datetime.date(2023, 1, 1),
        to_date=datetime.date(2023, 12, 31),
        country="DE",
        company="ABC Corp",
    )

    # Assertions
    assert response == {"data": "some data"}
    mock_session.get.assert_called_once_with(
        url="https://agsi.gie.eu/api/",
        params={
            "from": datetime.date(2023, 1, 1),
            "to": datetime.date(2023, 12, 31),
            "page": 1,
            "size": 30,
            "country": "DE",
            "company": "ABC Corp",
        },
    )


def test_query_storage_invalid_size(gie_client, mock_session):
    # Mocking the session
    api_type = APIType.AGSI

    with pytest.raises(
        ValueError, match="`size` param must be between 1 and 300"
    ):
        gie_client.query_storage(
            api_type=api_type,
            size=400,  # Invalid size, should trigger ValueError
        )


# ===== Test query_unavailability =====


def test_query_unavailability_success(gie_client, mock_session):
    # Mocking the API response and session
    mock_session.get.return_value.json.return_value = {"data": "some data"}
    api_type = APIType.AGSI

    response = gie_client.query_unavailability(
        api_type=api_type,
        page=1,
        size=30,
        from_date=datetime.date(2023, 1, 1),
        to_date=datetime.date(2023, 12, 31),
        country="DE",
        company="ABC Corp",
        end_flag="Confirmed",
        type="Unplanned",
    )

    # Assertions
    assert response == {"data": "some data"}
    mock_session.get.assert_called_once_with(
        url="https://agsi.gie.eu/api/unavailability",
        params={
            "from": datetime.date(2023, 1, 1),
            "to": datetime.date(2023, 12, 31),
            "page": 1,
            "size": 30,
            "country": "DE",
            "company": "ABC Corp",
            "end_flag": "Confirmed",
            "type": "Unplanned",
        },
    )


def test_query_unavailability_invalid_size(gie_client, mock_session):
    # Mocking the session
    api_type = APIType.AGSI

    with pytest.raises(
        ValueError,
        match="`end_flag` must be one of",
    ):
        gie_client.query_unavailability(
            api_type=api_type,
            end_flag="wrong flag",  # Invalid flag, should trigger ValueError
        )
