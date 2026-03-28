"""
PyPI Registry integration for stalecheck.

This module provides functions to interact with the PyPI JSON API to fetch
package metadata, specifically the latest stable version of a package.
"""
import httpx

from stalecheck.devsettings import get_settings
from stalecheck.logger import setup_logger

settings = get_settings("dev")

logger = setup_logger(verbose=True)


def get_latest_pypi_version(package: str) -> str | None:
    """
    Fetch the latest version of a package from PyPI.

    Queries the PyPI JSON API for the specified package and extracts the
    latest version string from the 'info' section.

    :param package: The name of the package to query.
    :returns: The latest version string if found, otherwise None.
    """
    url = f"https://pypi.org/pypi/{package}/json"
    with httpx.Client() as client:
        logger.info(f"sent request to pypi version for {package}...")
        r = client.get(url, timeout=settings.REQUEST_TIMEOUT)
        logger.info("response from pypi retrieved")
        if r.status_code != 200:
            return None

        version = r.json()["info"]["version"]
        logger.info(f"latest version of {package}: {version}")
        return version
