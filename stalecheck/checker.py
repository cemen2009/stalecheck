"""
Checker module for the stalecheck package.

This module exposes the `Checker` class, which serves as the main entry point
for analyzing package dependency files to identify outdated or 'stale'
dependencies.
"""

from packaging.requirements import Requirement
from packaging.version import Version
from pathlib import Path

from stalecheck.logger import setup_logger
from .models import Package, VersionSeverity
from .parsers import get_parser
from .registries import get_registry, Registry


class Checker:
    """
    Coordinates the process of parsing dependency files and checking
    their version status against remote package registries.
    """

    def __init__(self):
        self.logger = setup_logger(verbose=True)

    def run(self, file: Path) -> list[Package]:
        get_latest_version_of_package = get_registry(Registry.pypi)

        parser = get_parser(file)
        packages: list[Requirement] = parser.get_packages()
        results: list[Package] = []

        for requirement in packages:
            name = requirement.name
            latest = get_latest_version_of_package(requirement.name)

            installed_str = list(requirement.specifier)[0].version
            installed = Version(installed_str)

            severity = self._compare_versions(installed, latest)

            package = Package(
                name=name,
                installed=str(installed),
                latest=str(latest),
                severity=severity,
            )
            results.append(package)

        return results

    def _compare_versions(self, installed: Version, latest: Version) -> VersionSeverity:
        if installed >= latest:
            return VersionSeverity.ok
        elif latest.major - installed.major >= 2:
            return VersionSeverity.ancient
        elif latest.minor - installed.minor == 1:
            return VersionSeverity.major
        return VersionSeverity.minor
