from dataclasses import dataclass
from enum import StrEnum, auto


class VersionSeverity(StrEnum):
    ok = auto()
    minor = auto()
    major = auto()
    ancient = auto()
    unknown = auto()


@dataclass
class Package:
    name: str
    installed: str
    latest: str
    severity: VersionSeverity
