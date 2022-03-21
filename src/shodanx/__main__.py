import shodanx
import asyncio
import functools
import rich_click

from typing import Callable

from rich.console import Console

from .consts import T


console = Console()

click = rich_click
click.rich_click.USE_RICH_MARKUP = True


def asyncf(func: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(func)
    def wrap(*args, **kwargs) -> T:
        return asyncio.run(func(*args, **kwargs))  # type: ignore
    return wrap


@click.group()
def cli() -> None: ...


@cli.command()
@click.argument("host")
@click.option("--as-json", is_flag=True)
@asyncf
async def internetdb(host: str, as_json: bool = False) -> None:
    """ Get InternetDB info """
    async with shodanx.ShodanX() as shodan:
        console.print(await shodan.internetdb(host, as_json=as_json))


@cli.command()
@click.argument("host")
@click.option("--as-json", is_flag=True)
@asyncf
async def host(host: str, as_json: bool = False) -> None:
    """ Get host info """
    async with shodanx.ShodanX() as shodan:
        console.print(await shodan.host(host, as_json=as_json))


if __name__ == "__main__":
    cli()
