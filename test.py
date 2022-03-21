import asyncio
from rich.console import Console

from src.shodanx import ShodanX


console = Console()
client = ShodanX()


async def main():
    console.print(await client.host("1.1.1.1"))

asyncio.run(main())
