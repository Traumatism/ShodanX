import os
import httpx
import asyncer

from typing import Optional, Dict

from shodan.cli.settings import SHODAN_CONFIG_DIR
from .consts import SHO_URL


def load_api_key() -> str:
    """ Load the API key from the environment """

    if os.environ.get("SHODAN_API_KEY"):
        return os.environ["SHODAN_API_KEY"]

    keyfile = f"{os.path.expanduser(SHODAN_CONFIG_DIR)}/api_key"

    if not os.path.exists(keyfile):
        raise FileNotFoundError(f"API key file not found at {keyfile}")

    if not oct(os.stat(keyfile).st_mode).endswith("600"):
        os.chmod(keyfile, 0o600)

    with open(keyfile, 'r') as f:
        return f.read().strip()


def get(
    path: str,
    params: Optional[Dict] = None,
    key: str = load_api_key(),
    base_url: str = SHO_URL
) -> httpx.Response:
    """ Get a response from the API """

    key = load_api_key()

    if params is None:
        params = {}

    params["key"] = key

    response = httpx.get(f"{base_url}{path}", params=params)
    response.raise_for_status()

    return response


async def async_get(
    path: str,
    params: Optional[Dict] = None,
    key: str = load_api_key(),
    base_url: str = SHO_URL
) -> httpx.Response:
    """ Get a response from the API """
    return await asyncer.asyncify(get)(path, params, key, base_url)
