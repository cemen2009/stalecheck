from enum import StrEnum, auto
from typing import Callable

from packaging.version import Version

from .pypi import get_latest_pypi_version

REGISTRIES_MAP = {
    "pypi": get_latest_pypi_version,
}


class Registry(StrEnum):
    pypi = auto()


def get_registry(name: Registry) -> Callable[[str], Version | None]:
    registry_func = REGISTRIES_MAP.get(name)
    if registry_func is None:
        raise ValueError(f"Registry {name} is not supported.")

    return registry_func
