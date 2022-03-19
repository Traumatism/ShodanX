import os
import shodanx
import asyncio
import functools

import rich_click as click

from typing import Callable, TypeVar

from rich.console import Console


click.rich_click.USE_RICH_MARKUP = True


console = Console()
client = shodanx.Client(os.environ["SHODAN_API_KEY"])


T = TypeVar("T")


def async_f(func: Callable[..., T]) -> Callable[..., T]:
    """ Add async support to click. """

    @functools.wraps(func)
    def wrap(*args, **kwargs) -> T:
        return asyncio.run(
            func(*args, **kwargs)  # type: ignore
        )

    return wrap


@click.group()
def cli() -> None: ...


@cli.command()
@click.argument("query")
@click.option("--page", default=1, type=int)
@click.option("--limit", default=100, type=int)
@async_f
async def search(query: str, page: int, limit: int) -> None:
    """ Search a query """
    for host in (await client.search(query, page, limit)):
        print(host)

    await client.close()


@cli.command()
@click.argument("target")
@async_f
async def host(target: str) -> None:
    """ Get host info """
    host = await client.host(target)

    console.print(host)

    await client.close()
