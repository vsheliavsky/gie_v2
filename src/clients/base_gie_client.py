import datetime
from abc import ABC, abstractmethod
from typing import Literal

import aiohttp
import requests

from src.api_models.platform import APIType
from src.utils.cutom_types import ParamDict, Json


class BaseGieClient(ABC):
    """
    Abstract base class for interacting with the GIE (Gas Infrastructure Europe) API.

    This class provides the foundational structure for GIE clients, handling API keys, session management, and providing
    abstract methods that must be implemented by subclasses to query various endpoints of the API, such as storage data, unavailability
    data, EIC listings, and news items.

    Attributes:
        api_key (str): The API key used to authenticate with the GIE API.
        session (requests.Session | aiohttp.ClientSession): The HTTP session used for making synchronous or asynchronous API requests.

    Methods:
        fetch: Abstract method to fetch data from a specified endpoint with various filters.
        query_storage: Abstract method to query storage data with filters for date, type, country, and facility.
        query_unavailability: Abstract method to query unavailability data with filters for planned/unplanned outages.
        query_eic_listing: Abstract method to query the EIC listing, optionally fetching the complete list.
        query_news_listing: Abstract method to query news listings or a specific news item.
        close_session: Abstract method to close the HTTP session.
    """  # noqa: E501

    def __init__(
        self, api_key: str, session: requests.Session | aiohttp.ClientSession
    ) -> None:
        self.api_key = api_key
        self.session = session
        # TODO: Discuss Logging

    @property
    def api_key(self) -> str:
        return self.__api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        if not value:
            raise ValueError("API key is missing?")
        self.__api_key = value

    def _validate_session_headers(self) -> None:
        """Validate that the session headers contain the correct API key."""
        if "x-key" not in self.session.headers:
            raise ValueError("Session headers must include 'x-key'")
        if self.session.headers["x-key"] != self.api_key:
            raise ValueError("Session headers include incorrect 'x-key'")

    @abstractmethod
    def fetch(
        self,
        api_type: APIType,
        params: ParamDict,
        endpoint: str | None,
    ) -> Json:
        """
        Helper function to fetch data from different endpoints of the API based on the provided filters and parameters.

        Parameters:
            api_type (APIType): The type of API to fetch data from.
            page (int | str | None): The page number or identifier for paginated results.
            reverse (str | bool | None): Whether to reverse the order of the results. Can be a boolean or string representation of a boolean.
            size (int | None): The number of items per page or batch to retrieve.
            from_date (datetime.datetime | str | None): The starting date for filtering results, in datetime or string format.
            to_date (datetime.datetime | str | None): The ending date for filtering results, in datetime or string format.
            start (datetime.datetime | str | None): The start date or time for the data query.
            end (datetime.datetime | str | None): The end date or time for the data query.
            date (datetime.datetime | str | None): A specific date to query data for, in datetime or string format.
            updated (datetime.datetime | str | None): The last updated date to filter results by.
            type (str | None): The type of data or entity to filter results by.
            end_flag (str | None): An optional flag to indicate if the result set has an ending marker.
            country (str | None): The country to filter the results by.
            company (str | None): The company name to filter the results by.
            facility (str | None): The facility to filter the results by.
            params (dict[str, str] | None): Additional parameters to pass to the API as key-value pairs.
            endpoint (str | None): The specific API endpoint to query.
            news_url_item (int | str | None): An item identifier or URL related to the news entry to fetch data for.

        Returns:
            dict[str, Any]: A dictionary containing the fetched data from the API.
        """  # noqa: E501
        ...

    @abstractmethod
    def query_storage(
        self,
        api_type: APIType,
        page: int | str | None,
        reverse: str | bool | None,
        size: int | None,
        from_date: datetime.datetime | str | None,
        to_date: datetime.datetime | str | None,
        date: datetime.datetime | str | None,
        updated: datetime.datetime | str | None,
        type: Literal["EU", "NE", "AI"] | None,
        country: str | None,
        company: str | None,
        facility: str | None,
    ) -> Json:
        """
        Query storage data based on the provided filters and parameters.

        Parameters:
            api_type (APIType): The type of API from which data is being queried.
            page (int | str | None): The page number or identifier for paginated results.
            reverse (str | bool | None): Whether to reverse the order of the results. Can be a boolean or string representation of a boolean.
            size (int | None): The number of items per page or batch to retrieve.
            from_date (datetime.datetime | str | None): The starting date for filtering results, in datetime or string format.
            to_date (datetime.datetime | str | None): The ending date for filtering results, in datetime or string format.
            date (datetime.datetime | str | None): A specific date to query data for, in datetime or string format.
            updated (datetime.datetime | str | None): The last updated date to filter results by.
            type (Literal["EU", "NE", "AI"] | None): The type of data to filter by, with options being "EU", "NE", or "AI".
            country (str | None): The country to filter the results by.
            company (str | None): The company name to filter the results by. Note that a `country` parameter must be passed to use this.
            facility (str | None): The facility to filter the results by. Note that both `country` and `company` parameters must be passed to use this.

        Returns:
            dict[str, Any]: A dictionary containing the fetched data from the API.
        """  # noqa: E501
        ...

    @abstractmethod
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
        """
        Query the unavailability data based on the provided filters and parameters.

        Parameters:
            api_type (APIType): The type of API from which data is being queried.
            page (int | str | None): The page number or identifier for paginated results.
            reverse (str | bool | None): Whether to reverse the order of the results. Can be a boolean or string representation of a boolean.
            size (int | None): The number of items per page or batch to retrieve.
            from_date (datetime.datetime | str | None): The starting date for filtering results, in datetime or string format.
            to_date (datetime.datetime | str | None): The ending date for filtering results, in datetime or string format.
            start (datetime.datetime | str | None): The start date or time for the unavailability period being queried.
            end (datetime.datetime | str | None): The end date or time for the unavailability period being queried.
            type (Literal["Planned", "Unplanned"]): The type of unavailability, either "Planned" or "Unplanned".
            end_flag (Literal["confirmed", "estimate"]): The flag indicating if the unavailability end is confirmed or an estimate.
            country (str | None): The country to filter the results by.
            company (str | None): The company name to filter the results by.
            facility (str | None): The facility to filter the results by.

        Returns:
            dict[str, Any]: A dictionary containing the queried unavailability data.
        """  # noqa: E501
        ...

    @abstractmethod
    def query_eic_listing(
        self, api_type: APIType, complete: bool = False
    ) -> Json:
        """
        Query the EIC (Energy Identification Code) listing based on the provided API type.

        Parameters:
            api_type (APIType): The type of API from which to query the EIC listing.
            complete (bool, optional): Whether to retrieve the complete EIC listing. Defaults to False.

        Returns:
            dict[str, Any]: The queried EIC listing data, the structure of which depends on the API being queried.
        """  # noqa: E501
        ...

    @abstractmethod
    def query_news_listing(
        self, api_type: APIType, news_url: str | None
    ) -> Json:
        """
        Query the news listing or a specific news item based on the provided API type and URL.

        Parameters:
            api_type (APIType): The type of API from which to query the news listing.
            news_url (str | None): The URL of a specific news item to retrieve. If None, the method will return a listing of news items.

        Returns:
            dict[str, Any]: A dictionary containing the news data. If `news_url` is provided, returns the specific news item. Otherwise, returns a list of news items.
        """  # noqa: E501
        ...
