from httpx import AsyncClient, Response
from typing import Dict, Optional, Generator

from .responses.host import HostInfo


BASE_URL = "https://api.shodan.io"


class Client:
    """ ShodanX API client """

    def __init__(self, api_key: str) -> None:
        """ Initialize the client """

        self.api_key = api_key

        self.client = AsyncClient(base_url=BASE_URL)

    async def get(self, path: str, params: Optional[Dict] = None) -> Response:
        """ Make a GET request """

        if params is None:
            params = {}

        params["key"] = self.api_key

        return await self.client.get(path, params=params)

    async def post(
        self, path: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Response:
        """ Make a POST request """

        if data is None:
            data = {}

        if params is None:
            params = {}

        params["key"] = self.api_key

        return await self.client.post(
            path,
            data=data,  # type: ignore
            params=params
        )

    async def close(self) -> None:
        """ Close the client """
        await self.client.aclose()

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def host(self, target: str) -> HostInfo:
        """ Get host info """
        return HostInfo(**(await self.get(f"/shodan/host/{target}")).json())

    async def search(
        self, query: str, page: int = 1, limit: int = 100
    ) -> Generator[HostInfo, None, None]:
        """ Search for hosts """
        response = await self.get(
            "/shodan/host/search",
            params={"query": query, "page": page, "limit": limit}
        )

        return (
            HostInfo(**host) for host in response.json()["matches"]
        )

    async def count(self, query: str) -> int:
        """ Count the number of hosts """
        response = await self.get(
            "/shodan/host/count", params={"query": query}
        )

        return response.json()["total"]
