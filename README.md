# ShodanX
_Supposed to be a better Shodan API wrapper_

## Install

`pip install git+https://github.com/traumatism/shodanx --upgrade`


## Example

```py
import asyncio
import shodanx
import os


KEY = os.environ['SHODAN_API_KEY']


def synchronous():
    """ ShodanX basic """

    with shodanx.Client(KEY) as client:
        host_info = client.host("1.1.1.1")
        query_results = client.search("apache")


async def asynchronous():
    """ ShodanX supports asyncio """

    async with shodanx.AsyncClient(KEY) as client:
        host_info = await client.host("1.1.1.1")
        query_results = await client.search("apache")


if __name__ == "__main__":
    synchronous()
    asyncio.run(asynchronous())

```
