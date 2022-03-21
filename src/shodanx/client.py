from typing import Dict, Union

from .models import InternetDB, Host, SearchResults
from .utils import async_get, load_api_key
from .consts import IDB_URL


class ShodanX:
    """ ShodanX asynchronous API client """

    def __init__(self, key: str = load_api_key()) -> None:
        self.key = key

    async def internetdb(
        self, host: str, as_json: bool = False
    ) -> Union[Dict, InternetDB]:
        """ Get InternetDB info """

        response = (await async_get(f"/{host}", base_url=IDB_URL, key=self.key)).json()

        if as_json:
            return response

        return InternetDB(**response)

    async def host(self, host: str, as_json: bool = False) -> Union[Dict, Host]:
        """ Get host info """
        response = (await async_get(f"/shodan/host/{host}", key=self.key)).json()

        if as_json:
            return response

        return Host(**response)

    async def search(
        self, query: str, page: int = 1, as_json: bool = False
    ) -> Union[Dict, SearchResults]:
        """ Search for hosts """
        response = (await async_get(
            "/shodan/host/search", params={"query": query, "page": page},
            key=self.key
        )).json()

        if as_json:
            return response

        return SearchResults(**response)

    async def count(self, query: str) -> int:
        """ Count the number of hosts """
        return (await async_get(
            "/shodan/host/count", params={"query": query}, key=self.key
        )).json()["total"]

    async def info(self):
        """ Get the account info """

    async def __aenter__(self) -> "ShodanX":
        return self

    async def __aexit__(self, *args) -> None:
        ...
