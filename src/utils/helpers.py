import datetime
from typing import Literal
from src.api_models.platform import APIType
from src.utils.cutom_types import ParamDict


def validate_dates(
    beginning: datetime.date | None = None, end: datetime.date | None = None
) -> None:
    """
    Validates that the beginning date is not after the end date.

    Args:
        beginning (datetime.date | None): The starting date. If None, no validation is performed.
        end (datetime.date | None): The ending date. If None, no validation is performed.

    Raises:
        ValueError: If both `beginning` and `end` are provided and `beginning` is after `end`.

    Example:
        validate_dates(datetime.date(2023, 1, 1), datetime.date(2022, 12, 31))
        # Raises ValueError: Starting date is after end date!
    """  # noqa: E501
    if (beginning and end) and (beginning > end):
        raise ValueError("Starting date is after end date!")


def validate_input_params(
    api_type: APIType,
    params: ParamDict,
    request_type: Literal["storage", "unavailability"],
) -> None:
    """
    Validates various input parameters for an API request, ensuring that they follow
    the required format and logical constraints.

    Args:
        api_type (APIType): The type of API being accessed. Must be an instance of the `APIType` enum.
        params (ParamDict): Dictionary containing the request parameters. Expected keys include:
            - "country" (str | None)
            - "company" (str | None)
            - "facility" (str | None)
            - "from_date" (datetime.date | None)
            - "to_date" (datetime.date | None)
            - "start" (datetime.date | None)
            - "end" (datetime.date | None)
            - "page" (int)
            - "size" (int)
            - "reverse" (Union[str, int, None])
            - "type" (str | None)
        request_type (Literal["storage", "unavailability"]): Specifies the type of request,
            which impacts validation rules for the `type` parameter.

    Raises:
        ValueError: If any of the following conditions are violated:
            - `api_type` is not an instance of `APIType`.
            - `country` is not provided when `company` or `facility` is given.
            - `facility` is provided but `company` is missing.
            - The date range in `from_date` and `to_date` or `start` and `end` is invalid.
            - `page` is less than or equal to 0.
            - `size` is not between 1 and 300.
            - `reverse` is not one of ["true", "false", 0, 1].
            - `type` is not one of the allowed values depending on the `request_type`.

    Example:
        validate_input_params(
            api_type=APIType.STORAGE,
            params={
                "country": "US",
                "company": "ABC Corp",
                "facility": None,
                "from_date": datetime.date(2023, 1, 1),
                "to_date": datetime.date(2023, 12, 31),
                "page": 1,
                "size": 100,
                "reverse": "true",
                "type": "EU"
            },
            request_type="storage"
        )
        # Validates the input without raising an exception.

        validate_input_params(
            api_type=APIType.STORAGE,
            params={"company": "ABC Corp", "facility": None, "page": 0},
            request_type="storage"
        )
        # Raises ValueError: `page` param must be more than 0.
    """
    # ----- ApiType checks -----
    if not isinstance(api_type, APIType):
        raise ValueError("The starting date must be before the end date.")

    # ----- facility checks -----
    if not params["country"] and (params["company"] or params["facility"]):
        raise ValueError(
            "`country` must be provided if `company` or `facility` are passed"
        )

    if params["facility"] and not params["company"]:
        raise ValueError("`company` must be provided if `facility` is passed")

    # ----- Date checks -----
    validate_dates(params.get("from_date", None), params.get("to_date", None))
    validate_dates(params.get("start", None), params.get("end", None))

    # ----- Page checks -----
    if params["page"] <= 0:
        raise ValueError("`page` param must be more than 0")

    # ----- Size checks -----
    if not (1 <= params["size"] <= 300):
        raise ValueError("`size` param must be between 1 and 300")

    # ----- Reverse checks ----
    reverse_options = ["true", "false", 0, 1]
    if params["reverse"] and (params["reverse"] not in reverse_options):
        raise ValueError(f"`reverse` must be one of: {reverse_options}")

    # ----- Type checks ----
    type_vars = (
        ["EU", "NE", "AI"]
        if request_type == "storage"
        else ["Unplanned", "Planned"]
    )
    if params["type"] and (params["type"] not in type_vars):
        raise ValueError(f"`type` must be one of {type_vars}")
