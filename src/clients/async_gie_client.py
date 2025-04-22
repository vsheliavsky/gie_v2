import datetime
from typing import Any, Literal
from urllib.parse import urljoin

import aiohttp
from src.api_models.platform import APIType
from src.clients.base_gie_client import BaseGieClient
from src.utils.helpers import validate_input_params


class GieClientAsynch(BaseGieClient):
    def __init__(
        self, api_key: str, session: aiohttp.ClientSession | None = None
    ) -> None:
        self.api_key = api_key

        if not session:
            session = aiohttp.ClientSession(headers={"x-key": self.api_key})
        self.session = session
        self._validate_session_headers()
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()

    async def fetch(
        self,
        api_type: APIType,
        params: dict[str, Any] | None = None,
        endpoint: str | None = None,
    ) -> dict[str, Any]:
        
        root_url = api_type.value
        final_url = urljoin(root_url, endpoint)

        final_params = (
            {k: v for k, v in params.items() if v} if params else dict()
        )

        async with self.session.get(url=final_url, params=final_params) as response:
            
            result = await response.json()  # type: ignore

            return result
        


    async def query_storage(
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
    ) -> dict[str, Any]:
        """
        Asynchronously queries the storage API endpoint with the specified parameters and returns the JSON response.

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
            dict[str, Any]: The JSON response from the API containing the storage data.

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

        return await self.fetch(api_type=api_type, params=params)

    async def query_unavailability(
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
        end_flag: Literal["Confirmed", "Estimate"] | None = None,
        country: str | None = None,
        company: str | None = None,
        facility: str | None = None,
    ) -> dict[str, Any]:
        """
        Asynchronously queries the unavailability API endpoint with the specified parameters and returns the JSON response.

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
            end_flag (Literal["Confirmed", "Estimate"] | None, optional): Specifies whether to filter by confirmed or estimated end dates.
                Defaults to None.
            country (str | None, optional): Country code to filter results. Defaults to None.
            company (str | None, optional): Company name to filter results. Defaults to None.
            facility (str | None, optional): Facility name to filter results. Defaults to None.

        Returns:
            dict[str, Any]: The JSON response from the unavailability API.

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
        return await self.fetch(
            api_type=api_type, params=params, endpoint="unavailability"
        )

    async def query_eic_listing(
        self, api_type: APIType, show_listing: bool = False
    ) -> dict[str, Any]:
        """
        Asynchronously queries the EIC listing or general API information and returns the JSON response.

        Args:
            api_type (APIType): The type of API being queried, determining the base URL.
            show_listing (bool, optional): If True, queries the EIC listing. If False, retrieves general information.
                Defaults to False.

        Returns:
            dict[str, Any]: The JSON response from the API.

        Raises:
            requests.RequestException: If the API request fails due to network issues or other errors.

        Example:
            # Asynchronously query the EIC listing
            response = query_eic_listing(api_type=APIType.AGSI, show_listing=True)

            # Asynchronously query general API information
            response = query_eic_listing(api_type=APIType.AGSI, show_listing=False)
        """  # noqa: E501

        params = {"show": "listing"} if show_listing else None
        return await self.fetch(api_type=api_type, params=params, endpoint="about")

    async def query_news_listing(
        self, api_type: APIType, news_url: str | None = None
    ) -> dict[str, Any]:
        """
        Asynchronously queries the news listing or specific news based on the provided URL and returns the JSON response.

        Args:
            api_type (APIType): The type of API being queried, determining the base URL.
            news_url (str | None, optional): The URL of the specific news item to query. If None, retrieves the general news listing.
                Defaults to None.

        Returns:
            dict[str, Any]: The JSON response from the news API.

        Raises:
            requests.RequestException: If the API request fails due to network issues or other errors.

        Example:
            # Asynchronously query the general news listing
            response = query_news_listing(api_type=APIType.AGSI)

            # Asynchronously query a specific news item by URL
            response = query_news_listing(api_type=APIType.AGSI, news_url="371616")
        """  # noqa: E501
        params = {"url": news_url} if news_url else None
        return await self.fetch(api_type=api_type, params=params, endpoint="news")
