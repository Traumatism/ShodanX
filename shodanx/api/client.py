import httpx

from typing import AsyncGenerator, Dict, Generator

from .responses.host import HostInfo


BASE_URL = "https://api.shodan.io"


class Client:
    """ ShodanX API client """

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = httpx.Client(base_url=BASE_URL)

    @property
    def params(self) -> Dict:
        return {"key": self.api_key}

    def close(self) -> None:
        return self.client.close()

    def host(self, ip: str) -> HostInfo:
        """ Get host info """
        response = self.client.get(f"/host/{ip}", params=self.params)
        response.raise_for_status()

        return HostInfo(**response.json())

    def search(
        self, query: str, page: int = 1, limit: int = 100
    ) -> Generator[HostInfo, None, None]:
        params = self.params.copy()

        params["query"] = query
        params["page"] = page
        params["limit"] = limit

        response = self.client.get("/shodan/host/search", params=params)
        response.raise_for_status()

        for host in response.json()["matches"]:
            yield HostInfo(**host)

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *args) -> None:
        self.close()


class AsyncClient(Client):
    """ ShodanX asynchronous API client """

    def __init__(self, api_key: str) -> None:
        """ Initialize the client """
        super().__init__(api_key)

        self.client = httpx.AsyncClient(base_url=BASE_URL)

    async def close(self) -> None:
        """ Close the client """
        await self.client.aclose()

    async def host(self, target: str) -> HostInfo:
        """ Get host info """
        response = await self.client.get(
            f"/shodan/host/{target}", params=self.params
        )
        response.raise_for_status()

        return HostInfo(**response.json())

    async def search(
        self, query: str, page: int = 1, limit: int = 100
    ) -> AsyncGenerator[HostInfo, None]:
        """ Search for hosts """
        params = self.params.copy()

        params["query"] = query
        params["page"] = page
        params["limit"] = limit

        response = await self.client.get("/shodan/host/search", params=params)
        response.raise_for_status()

        for host in response.json()["matches"]:
            yield HostInfo(**host)

    async def count(self, query: str) -> int:
        """ Count the number of hosts """
        params = self.params.copy()
        params["query"] = query

        response = await self.client.get("/shodan/host/count", params=params)
        response.raise_for_status()

        return response.json()["total"]

    async def info(self):
        """ Get the account info """

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()
