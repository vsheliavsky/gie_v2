# pyright: basic
import datetime
from unittest.mock import MagicMock, AsyncMock, patch
import aiohttp

import pandas.core.frame
import pytest_asyncio

import pytest
from src.api_models.platform import APIType
from src.clients.async_gie_client import GieClientAsynch

# ===== Fixture setup =====

@pytest.fixture
def valid_api_key():
    return "valid_api_key"


@pytest.fixture
def wrong_api_key():
    return "wrong_api_key"


@pytest_asyncio.fixture
def mock_session():
    session = AsyncMock(aiohttp.ClientSession)
    session.headers = dict()
    
    return session


@pytest_asyncio.fixture
def gie_asynch_client(mock_session, valid_api_key):
    mock_session.headers["x-key"] = valid_api_key
    return GieClientAsynch(api_key=valid_api_key, session=mock_session)

# ===== Test class instantiation =====
@pytest.mark.asyncio
async def test_valid_session(mock_session, valid_api_key):
    mock_session.headers["x-key"] = valid_api_key
    client = GieClientAsynch(api_key=valid_api_key, session=mock_session)

    assert client.session.headers["x-key"] == valid_api_key
    assert client.api_key == valid_api_key

@pytest.mark.asyncio
async def test_missing_header(mock_session, valid_api_key):
    with pytest.raises(
        ValueError, match="Session headers must include 'x-key'"
    ):
        GieClientAsynch(api_key=valid_api_key, session=mock_session)

@pytest.mark.asyncio
async def test_incorrect_header(mock_session, valid_api_key, wrong_api_key):
    session = mock_session
    session.headers["x-key"] = wrong_api_key
    with pytest.raises(
        ValueError, match="Session headers include incorrect 'x-key'"
    ):
        GieClientAsynch(api_key=valid_api_key, session=session)     

# ===== Test fetch =====
@pytest.mark.asyncio
async def test_fetch_success(valid_api_key):
    api_type = APIType.AGSI
    params = {"param1": "value1"}
    endpoint = "test_endpoint"
    expected_response = {"result": "success"}
    expected_url = "https://agsi.gie.eu/api/test_endpoint"
    expected_params = {"param1": "value1"}

    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value=expected_response)

    mock_get = AsyncMock()
    mock_get.__aenter__.return_value = mock_response
    mock_get.__aexit__.return_value = AsyncMock()

    mock_session = MagicMock()
    mock_session.get.return_value = mock_get
    mock_session.headers = {"x-key": valid_api_key}

    client = GieClientAsynch(api_key=valid_api_key, session=mock_session)

    result = await client.fetch(api_type=api_type, params=params, endpoint=endpoint)

    assert result == expected_response
    mock_session.get.assert_called_once_with(url=expected_url, params=expected_params)
    mock_response.json.assert_awaited_once()
    
    
# ===== Test query_storage =====

@pytest.mark.asyncio
async def test_query_storage_success(gie_asynch_client, mock_session):
    api_type = APIType.AGSI

    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={"data": "some data"})

    mock_context = AsyncMock()
    mock_context.__aenter__.return_value = mock_response
    mock_session.get.return_value = mock_context

    response = await gie_asynch_client.query_storage(
        api_type=api_type,
        page=1,
        size=30,
        from_date=datetime.date(2023, 1, 1),
        to_date=datetime.date(2023, 12, 31),
        country="DE",
        company="ABC Corp",
    )

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
    
    
@pytest.mark.asyncio
async def test_query_storage_invalid_size(gie_asynch_client):
    api_type = APIType.AGSI

    with pytest.raises(ValueError, match="`size` param must be between 1 and 300"):
        await gie_asynch_client.query_storage(
            api_type=api_type,
            size=400,  # Invalid size, should trigger ValueError
        )

# ===== Test query_unavailability =====

@pytest.mark.asyncio
async def test_query_unavailability_success(gie_asynch_client, mock_session):
    api_type = APIType.AGSI

    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={"data": "some data"})

    mock_context = AsyncMock()
    mock_context.__aenter__.return_value = mock_response
    mock_session.get.return_value = mock_context

    response = await gie_asynch_client.query_unavailability(
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

@pytest.mark.asyncio
async def test_query_unavailability_invalid_size(gie_asynch_client):
    api_type = APIType.AGSI

    with pytest.raises(ValueError, match="`end_flag` must be one of"):
        await gie_asynch_client.query_unavailability(
            api_type=api_type,
            end_flag="wrong flag",  # Invalid flag, should trigger ValueError
        )