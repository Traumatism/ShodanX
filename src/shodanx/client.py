import httpx

from typing import AsyncGenerator, Dict, Generator

from shodanx.utils import load_api_key

from .models import InternetDB, HostInfo


BASE_URL = "https://api.shodan.io"
IDB_URL = "https://internetdb.shodan.io"


class Client:
    """ ShodanX API client """

    def __init__(self, api_key: str = load_api_key()) -> None:
        self.api_key = api_key
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)

    @property
    def params(self) -> Dict:
        return {"key": self.api_key}

    def close(self) -> None:
        return self.client.close()

    def internetdb(self, ip: str) -> InternetDB:
        """ Get InternetDB info """

        with httpx.Client(base_url=IDB_URL) as client:
            response = client.get(f"{ip}")

        return InternetDB(**response.json())

    def host(self, host: str) -> HostInfo:
        """ Get host info """
        response = self.client.get(f"/shodan/host/{host}", params=self.params)
        response.raise_for_status()
        return HostInfo(**response.json())

    def search(self, query: str, page: int = 1) -> Generator[HostInfo, None, None]:
        params = self.params.copy()

        params["query"] = query
        params["page"] = page

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

    def __init__(self, api_key: str = load_api_key()) -> None:
        """ Initialize the client """
        super().__init__(api_key)

        self.client = httpx.AsyncClient(base_url=BASE_URL, timeout=30)

    async def close(self) -> None:
        """ Close the client """
        await self.client.aclose()

    async def internetdb(self, ip: str) -> InternetDB:
        """ Get InternetDB info """
        async with httpx.AsyncClient(base_url=IDB_URL) as client:
            response = await client.get(f"{ip}")

        return InternetDB(**response.json())

    async def host(self, target: str) -> HostInfo:
        """ Get host info """
        response = await self.client.get(f"/shodan/host/{target}", params=self.params)
        response.raise_for_status()

        return HostInfo(**response.json())

    async def search(self, query: str, page: int = 1) -> AsyncGenerator[HostInfo, None]:
        """ Search for hosts """
        params = self.params.copy()
        params["query"] = query
        params["page"] = page

        response = await self.client.get("/shodan/host/search", params=params)
        response.raise_for_status()

        return (HostInfo(**host) for host in response.json()["matches"])

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
