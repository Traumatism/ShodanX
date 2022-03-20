from typing import Dict

from .models import InternetDB, HostInfo
from .utils import get, async_get, load_api_key


IDB_URL = "https://internetdb.shodan.io"


class Client:
    """ ShodanX API client """

    def __init__(self, key: str = load_api_key()) -> None:
        self.key = key

    def internetdb(self, ip: str) -> InternetDB:
        """ Get InternetDB info """
        return InternetDB(**get(f"{ip}", base_url=IDB_URL, key=self.key).json())

    def host(self, host: str) -> HostInfo:
        """ Get host info """
        return HostInfo(**get(f"/shodan/host/{host}", key=self.key).json())

    def search(self, query: str, page: int = 1) -> Dict:
        """ Search for hosts """
        return get(
            "/shodan/host/search", params={"query": query, "page": page}, key=self.key
        ).json()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *args) -> None:
        ...


class AsyncClient(Client):
    """ ShodanX asynchronous API client """

    async def internetdb(self, ip: str) -> InternetDB:
        """ Get InternetDB info """
        return InternetDB(**(
            await async_get(
                f"{ip}",
                base_url=IDB_URL,
                key=self.key
            )
        ).json())

    async def host(self, target: str) -> HostInfo:
        """ Get host info """
        return HostInfo(**(
            await async_get(
                f"/shodan/host/{target}",
                key=self.key
            )
        ).json())

    async def search(self, query: str, page: int = 1) -> Dict:
        """ Search for hosts """
        return (await async_get(
            "/shodan/host/search",
            params={"query": query, "page": page},
            key=self.key
        )).json()

    async def count(self, query: str) -> int:
        """ Count the number of hosts """
        return (await async_get(
            "/shodan/host/count",
            params={"query": query}, key=self.key
        )).json()["total"]

    async def info(self):
        """ Get the account info """

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, *args) -> None:
        ...
