import typing

from shodan.cli.settings import SHODAN_CONFIG_DIR

T = typing.TypeVar("T")

IDB_URL = "https://internetdb.shodan.io"
SHODAN_URL = "https://api.shodan.io"

__all__ = ["IDB_URL", "SHODAN_URL", "SHODAN_CONFIG_DIR", "T"]
