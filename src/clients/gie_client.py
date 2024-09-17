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
        """
        Client class for interacting with the GIE API.

        This class handles API requests and manages the API session. It requires an API key for authentication.
        If a custom `requests.Session` is not provided, a new session is created with the API key set in the headers.

        Attributes:
            api_key (str): The API key used for authentication with the GIE API.
            session (requests.Session): The `requests.Session` object used for making HTTP requests.
                If not provided, a new session is created with the API key set in the headers.

        Example:
            # Create a GieClient instance with a custom session
            session = requests.Session()
            session.headers["x-key"] = "your_api_key"
            client = GieClient(api_key="your_api_key", session=session)

            # Create a GieClient instance with a new session
            client = GieClient(api_key="your_api_key")
        """  # noqa: E501
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
        """  # noqa: E501
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
        Queries the storage API endpoint with the specified parameters and returns the JSON response.

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
        """  # noqa: E501
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
        page: int = 1,
        reverse: Literal["true", "false", 0, 1] | None = None,
        size: int | None = 30,
        from_date: datetime.date | None = None,
        to_date: datetime.date | None = None,
        start: datetime.date | None = None,
        end: datetime.date | None = None,
        updated: datetime.date | None = None,
        type: Literal["Planned", "Unplanned"] | None = None,
        end_flag: Literal["confirmed", "estimate"] | None = None,
        country: str | None = None,
        company: str | None = None,
        facility: str | None = None,
    ) -> Json:
        """
        Queries the unavailability API endpoint with the specified parameters and returns the JSON response.

        Args:
            api_type (APIType): The type of API being queried, determining the base URL.
            page (int, optional): The page number for pagination. Defaults to 1.
            reverse (Literal["true", "false", 0, 1] | None, optional): Specifies whether to reverse the results.
                Accepts "true", "false", 0, or 1. Defaults to None.
            size (int | None, optional): Number of results per page. Must be between 1 and 300. Defaults to 30.
            from_date (datetime.date | None, optional): The start date for filtering results. Defaults to None.
            to_date (datetime.date | None, optional): The end date for filtering results. Defaults to None.
            start (datetime.date | None, optional): The start date of the unavailability period. Defaults to None.
            end (datetime.date | None, optional): The end date of the unavailability period. Defaults to None.
            updated (datetime.date | None, optional): Filter for data updated on this date. Defaults to None.
            type (Literal["Planned", "Unplanned"] | None, optional): The type of unavailability to query. Defaults to None.
            end_flag (Literal["confirmed", "estimate"] | None, optional): Specifies whether to filter by confirmed or estimated end dates.
                Defaults to None.
            country (str | None, optional): Country code to filter results. Defaults to None.
            company (str | None, optional): Company name to filter results. Defaults to None.
            facility (str | None, optional): Facility name to filter results. Defaults to None.

        Returns:
            Json: The JSON response from the unavailability API.

        Raises:
            ValueError: If any of the provided parameters fail validation.
            requests.RequestException: If the API request fails due to network issues or other errors.

        Example:
            response = query_unavailability(
                api_type=APIType.AGSI,
                page=1,
                size=50,
                from_date=datetime.date(2023, 1, 1),
                to_date=datetime.date(2023, 12, 31),
                country="DE",
                type="Planned"
            )
            # Queries the unavailability API endpoint and returns the response as JSON.
        """  # noqa: E501
        params = {
            "page": page,
            "reverse": reverse,
            "size": size,
            "from": from_date,
            "to": to_date,
            "start": start,
            "end": end,
            "updated": updated,
            "type": type,
            "end_flag": end_flag,
            "country": country,
            "company": company,
            "facility": facility,
        }

        validate_input_params(
            api_type=api_type, params=params, request_type="unavailability"
        )
        return self.fetch(
            api_type=api_type, params=params, endpoint="unavailability"
        )

    def query_eic_listing(
        self, api_type: APIType, show_listing: bool = False
    ) -> Json:
        """
        Queries the EIC listing or general API information and returns the JSON response.

        Args:
            api_type (APIType): The type of API being queried, determining the base URL.
            show_listing (bool, optional): If True, queries the EIC listing. If False, retrieves general information.
                Defaults to False.

        Returns:
            Json: The JSON response from the API.

        Raises:
            requests.RequestException: If the API request fails due to network issues or other errors.

        Example:
            # Query the EIC listing
            response = query_eic_listing(api_type=APIType.AGSI, show_listing=True)

            # Query general API information
            response = query_eic_listing(api_type=APIType.AGSI, show_listing=False)
        """  # noqa: E501

        params = {"show": "listing"} if show_listing else None
        return self.fetch(api_type=api_type, params=params, endpoint="about")

    def query_news_listing(
        self, api_type: APIType, news_url: str | None = None
    ) -> Json:
        """
        Queries the news listing or specific news based on the provided URL and returns the JSON response.

        Args:
            api_type (APIType): The type of API being queried, determining the base URL.
            news_url (str | None, optional): The URL of the specific news item to query. If None, retrieves the general news listing.
                Defaults to None.

        Returns:
            Json: The JSON response from the news API.

        Raises:
            requests.RequestException: If the API request fails due to network issues or other errors.

        Example:
            # Query the general news listing
            response = query_news_listing(api_type=APIType.AGSI)

            # Query a specific news item by URL
            response = query_news_listing(api_type=APIType.AGSI, news_url="371616")
        """  # noqa: E501
        params = {"url": news_url} if news_url else None
        return self.fetch(api_type=api_type, params=params, endpoint="news")
