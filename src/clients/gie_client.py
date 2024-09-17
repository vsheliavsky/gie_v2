# pyright: basic

import datetime
from typing import Literal
from urllib.parse import urljoin

import requests

from src.clients.base_gie_client import BaseGieClient
from src.api_models.platform import APIType
from src.utils.cutom_types import Json, ParamDict
from src.utils.helpers import validate_input_params


class GieClient(BaseGieClient):
    def __init__(
        self, api_key: str, session: requests.Session | None = None
    ) -> None:
        self.api_key = api_key

        if not session:
            session = requests.Session()
            session.headers = {"x-key": self.api_key}
        self.session = session
        self._validate_session_headers()

    def fetch(
        self,
        api_type: APIType,
        params: ParamDict | None = None,
        endpoint: str | None = None,
    ) -> Json:
        """
        Sends a GET request to a specified API endpoint with the provided parameters
        and returns the JSON response.

        Args:
            api_type (APIType): The type of API to interact with. Determines the root URL based on the `APIType` enum value.
            params (ParamDict | None): A dictionary of query parameters to include in the request.
                Only parameters with non-None values are sent. Defaults to None, in which case no parameters are included.
            endpoint (str | None): The specific API endpoint to append to the root URL. If None, the root URL is used.

        Returns:
            Json: The JSON response from the API.

        Raises:
            requests.RequestException: If the request fails due to network or other issues.

        Example:
            response = fetch(api_type=APIType.AGSI, params={"country": "DE"})
            # Sends a GET request to the constructed URL and returns the JSON response.
        """
        root_url = api_type.value
        final_url = urljoin(root_url, endpoint)

        final_params = (
            {k: v for k, v in params.items() if v} if params else dict()
        )

        response = self.session.get(url=final_url, params=final_params)

        return response.json()

    def query_storage(
        self,
        api_type: APIType,
        page: int = 1,
        reverse: Literal["true", "false", 0, 1] | None = None,
        size: int | None = 30,
        from_date: datetime.date | None = None,
        to_date: datetime.date | None = None,
        date: datetime.date | None = None,
        updated: datetime.date | None = None,
        type: Literal["EU", "NE", "AI"] | None = None,
        country: str | None = None,
        company: str | None = None,
        facility: str | None = None,
    ) -> Json:
        """
        Queries the storage API with the specified parameters and returns the JSON response.

        Args:
            api_type (APIType): The type of API being queried, which defines the base URL.
            page (int, optional): The page number for pagination. Defaults to 1.
            reverse (Literal["true", "false", 0, 1] | None, optional): Determines if the results should be reversed.
                Accepts "true", "false", 0, or 1. Defaults to None.
            size (int | None, optional): The number of results per page. Defaults to 30. Must be between 1 and 300.
            from_date (datetime.date | None, optional): The start date for the query filter. Defaults to None.
            to_date (datetime.date | None, optional): The end date for the query filter. Defaults to None.
            date (datetime.date | None, optional): A specific date for querying data. Defaults to None.
            updated (datetime.date | None, optional): A filter for querying data updated on this date. Defaults to None.
            type (Literal["EU", "NE", "AI"] | None, optional): The type of storage data to query. Defaults to None.
            country (str | None, optional): The country code to filter the results. Defaults to None.
            company (str | None, optional): The company name to filter the results. Defaults to None.
            facility (str | None, optional): The facility name to filter the results. Defaults to None.

        Returns:
            Json: The JSON response from the API containing the storage data.

        Raises:
            ValueError: If any of the provided parameters are invalid according to the validation rules.
            requests.RequestException: If the request fails due to network issues or other errors.

        Example:
            response = query_storage(
                api_type=APIType.AGSI,
                page=1,
                size=50,
                from_date=datetime.date(2023, 1, 1),
                to_date=datetime.date(2023, 12, 31),
                country="DE",
                company="ABC Corp"
            )
            # Returns the JSON response from the API with the specified filters.
        """
        params = {
            "from": from_date,
            "to": to_date,
            "date": date,
            "page": page,
            "reverse": reverse,
            "size": size,
            "updated": updated,
            "type": type,
            "country": country,
            "company": company,
            "facility": facility,
        }
        validate_input_params(
            api_type=api_type, params=params, request_type="storage"
        )
        return self.fetch(api_type=api_type, params=params)

    def query_unavailability(
        self,
        api_type: APIType,
        page: int | str | None,
        reverse: str | bool | None,
        size: int | None,
        from_date: datetime.datetime | str | None,
        to_date: datetime.datetime | str | None,
        start: datetime.datetime | str | None,
        end: datetime.datetime | str | None,
        type: Literal["Planned", "Unplanned"],
        end_flag: Literal["confirmed", "estimate"],
        country: str | None,
        company: str | None,
        facility: str | None,
    ) -> Json:
        pass

    def query_eic_listing(
        self, api_type: APIType, complete: bool = False
    ) -> Json:
        pass

    def query_news_listing(
        self, api_type: APIType, news_url: str | None
    ) -> Json:
        pass
