# ShodanX
_Supposed to be a better Shodan API wrapper_

## Install

`pip install git+github.com/traumatism/shodanx`


## Example
```py
import asyncio
import shodanx
import os


async def asynchronous():
    """ ShodanX supports asyncio """
    async with shodanx.AsyncClient() as client:
        host_info = await client.host("1.1.1.1")

        query_results = await client.search("apache")


def synchronous():
    """ ShodanX supports syncio """
    with shodanx.Client() as client:
        host_info = client.host("1.1.1.1")

        query_results = client.search("apache")


if __name__ == "__main__":
    synchronous()
    asyncio.run(asynchronous())

```