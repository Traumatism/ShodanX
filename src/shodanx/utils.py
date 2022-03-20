import os

from shodan.cli.settings import SHODAN_CONFIG_DIR


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
