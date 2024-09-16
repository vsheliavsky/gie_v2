# pyright: basic

import datetime
from typing import Literal
from urllib.parse import urljoin

import requests

from src.clients.base_gie_client import BaseGieClient
from src.api_models.platform import APIType
from src.utils.cutom_types import Json, ParamDict


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
        root_url = api_type.value
        final_url = urljoin(root_url, endpoint)

        final_params = (
            {k: v for k, v in params.items() if v} if params else dict()
        )

        response = self.session.get(url=final_url, params=final_params)

        return response.json()

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
        pass

    def query_eic_listing(
        self, api_type: APIType, complete: bool = False
    ) -> Json:
        pass

    def query_news_listing(
        self, api_type: APIType, news_url: str | None
    ) -> Json:
        pass
