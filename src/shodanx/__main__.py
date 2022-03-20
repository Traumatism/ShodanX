import os
import asyncio
import functools
import rich_click

from typing import Callable, TypeVar

from rich.console import Console

from .api import Client

console = Console()

click = rich_click

click.rich_click.USE_RICH_MARKUP = True

KEY = os.environ["SHODAN_API_KEY"]

T = TypeVar("T")


def desync(func: Callable[..., T]) -> Callable[..., T]:
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
def search(query: str, page: int, limit: int) -> None:
    """ Search a query """
    with Client(KEY) as client:
        for host in client.search(query, page, limit):
            print(host)


@cli.command()
@click.argument("host", metavar="<ip address>")
def host(target: str) -> None:
    """ Get host info """
    with Client(KEY) as client:
        console.print(client.host(target))


if __name__ == "__main__":
    cli()
