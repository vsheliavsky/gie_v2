import datetime

import pytest
from src.api_models.platform import APIType
from src.utils.helpers import validate_dates, validate_input_params


# ===== validate_dates =====
def test_validate_dates_valid_range():
    # Test valid date range
    beginning = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    assert validate_dates(beginning, end) is None  # Should not raise an error


def test_validate_dates_none_params():
    # Test with None values (no dates to compare)
    assert validate_dates(None, None) is None  # Should not raise an error


def test_validate_dates_valid_with_none():
    # Test with only one valid date (should not raise an error)
    assert validate_dates(datetime.date(2023, 1, 1), None) is None
    assert validate_dates(None, datetime.date(2023, 12, 31)) is None


def test_validate_dates_invalid_range():
    # Test invalid date range where beginning is after end
    beginning = datetime.date(2023, 12, 31)
    end = datetime.date(2023, 1, 1)
    with pytest.raises(ValueError, match="Starting date is after end date!"):
        validate_dates(beginning, end)


# ===== validate_input_params =====
def test_validate_input_params_valid():
    # Test with valid input parameters
    params = {
        "country": "US",
        "company": "ABC Corp",
        "facility": None,
        "from_date": datetime.date(2023, 1, 1),
        "to_date": datetime.date(2023, 12, 31),
        "start": None,
        "end": None,
        "page": 1,
        "size": 100,
        "reverse": "true",
        "type": "EU",
    }
    api_type = APIType.AGSI
    assert (
        validate_input_params(api_type, params, "storage") is None
    )  # Should not raise an error


def test_validate_input_params_missing_country():
    # Test missing country but with company or facility
    params = {
        "country": None,
        "company": "ABC Corp",
        "facility": None,
        "page": 1,
        "size": 100,
        "reverse": "true",
        "type": "EU",
    }
    api_type = APIType.AGSI
    with pytest.raises(
        ValueError,
        match="`country` must be provided if `company` or `facility` are passed",  # noqa: E501
    ):
        validate_input_params(api_type, params, "storage")


def test_validate_input_params_facility_without_company():
    # Test facility without company
    params = {
        "country": "US",
        "company": None,
        "facility": "Facility 1",
        "page": 1,
        "size": 100,
        "reverse": "true",
        "type": "EU",
    }
    api_type = APIType.AGSI
    with pytest.raises(
        ValueError, match="`company` must be provided if `facility` is passed"
    ):
        validate_input_params(api_type, params, "storage")


def test_validate_input_params_invalid_page():
    # Test invalid page (<= 0)
    params = {
        "country": "US",
        "company": "ABC Corp",
        "facility": None,
        "page": 0,
        "size": 100,
        "reverse": "true",
        "type": "EU",
    }
    api_type = APIType.AGSI
    with pytest.raises(ValueError, match="`page` param must be more than 0"):
        validate_input_params(api_type, params, "storage")


def test_validate_input_params_invalid_size():
    # Test invalid size (outside 1-300)
    params = {
        "country": "US",
        "company": "ABC Corp",
        "facility": None,
        "page": 1,
        "size": 301,  # Invalid size
        "reverse": "true",
        "type": "EU",
    }
    api_type = APIType.AGSI
    with pytest.raises(
        ValueError, match="`size` param must be between 1 and 300"
    ):
        validate_input_params(api_type, params, "storage")


def test_validate_input_params_invalid_reverse():
    # Test invalid reverse parameter
    params = {
        "country": "US",
        "company": "ABC Corp",
        "facility": None,
        "page": 1,
        "size": 100,
        "reverse": "invalid_value",  # Invalid reverse
        "type": "EU",
    }
    api_type = APIType.AGSI
    with pytest.raises(ValueError, match="`reverse` must be one of"):
        validate_input_params(api_type, params, "storage")


def test_validate_input_params_invalid_type():
    # Test invalid type depending on request_type
    params = {
        "country": "US",
        "company": "ABC Corp",
        "facility": None,
        "page": 1,
        "size": 100,
        "reverse": "true",
        "type": "InvalidType",  # Invalid type
    }
    api_type = APIType.AGSI
    with pytest.raises(ValueError, match="`type` must be one of"):
        validate_input_params(api_type, params, "storage")
