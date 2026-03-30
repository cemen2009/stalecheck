"""
PyPI Registry integration for stalecheck.

This module provides functions to interact with the PyPI JSON API to fetch
package metadata, specifically the latest stable version of a package.
"""

import httpx
from packaging.version import Version

from stalecheck.settings import get_settings
from stalecheck.logger import setup_logger

settings = get_settings("dev")

logger = setup_logger(verbose=True)


def get_latest_pypi_version(package: str) -> Version | None:
    """
    Fetch the latest version of a package from PyPI.

    Queries the PyPI JSON API for the specified package and extracts the
    latest version string from the 'info' section.

    :param package: The name of the package to query.
    :returns: The latest version string if found, otherwise None.
    """
    url = f"https://pypi.org/pypi/{package}/json"
    with httpx.Client() as client:
        logger.debug(f"Sent request to pypi version for {package}...")
        r = client.get(url, timeout=settings.REQUEST_TIMEOUT)
        logger.debug("Response from pypi retrieved")
        if r.status_code != 200:
            return None

        version_str = r.json()["info"]["version"]
        version = Version(version_str)
        logger.info(f"Latest version of {package}: {version}")
        return version
