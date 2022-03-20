import asyncio
import functools
import rich_click

from typing import Callable, TypeVar

from rich.console import Console

from .utils import load_api_key
from .client import Client, AsyncClient

console = Console()

click = rich_click
click.rich_click.USE_RICH_MARKUP = True

T = TypeVar("T")
KEY = load_api_key()


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
def search(query: str, page: int) -> None:
    """ Search a query """
    with Client(KEY) as client:
        for host in client.search(query, page):
            print(host)


@cli.command()
@click.argument("host", metavar="<ip address>")
def host(host: str) -> None:
    """ Get host info """
    with Client() as client:
        console.print(client.host(host))


@cli.command()
@click.argument("file", type=click.File("r"))
@desync
async def hosts(file: str) -> None:
    """ Get hosts info """

    async with AsyncClient() as client:
        lines = (line.strip() for line in file)

        results = asyncio.gather(
            asyncio.create_task(client.host(line)) for line in lines
        )

        for result in await results:
            console.print(result)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@desync
async def internetdb(file: str) -> None:
    """ Get hosts info """
    async with AsyncClient() as client:
        results = await asyncio.gather(*[
            asyncio.create_task(client.internetdb(line.strip()))
            for line in open(file, "r").readlines()
        ])

        for result in results:
            console.print(result)


if __name__ == "__main__":
    cli()
