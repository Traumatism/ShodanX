import os
import asyncio
import functools
import rich_click

from typing import Callable, TypeVar
from rich.console import Console

from .api import Client

click = rich_click
click.rich_click.USE_RICH_MARKUP = True
console = Console()

KEY = os.environ["SHODAN_API_KEY"]
T = TypeVar("T")


def async_f(func: Callable[..., T]) -> Callable[..., T]:
    """ Add async support to click with keeping return type """

    @functools.wraps(func)
    def wrap(*args, **kwargs) -> T:
        return asyncio.run(func(*args, **kwargs))  # type: ignore

    return wrap


@click.group()
def cli() -> None: ...


@cli.command()
@click.argument("query", metavar="<query>")
@click.option("--page", default=1, type=int)
@click.option("--limit", default=100, type=int)
@async_f
async def search(query: str, page: int, limit: int) -> None:
    """ Search a query """
    async with Client(KEY) as client:
        async for host in client.search(query, page, limit):
            print(host)


@cli.command()
@click.argument("host", metavar="<ip address>")
@async_f
async def host(target: str) -> None:
    """ Get host info """
    async with Client(KEY) as client:
        console.print(await client.host(target))
        await client.close()


if __name__ == "__main__":
    cli()
