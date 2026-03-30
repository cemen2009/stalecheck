"""
Parser for standard requirements.txt files.

This module provides the RequirementsParser class, which implements the Parser
protocol to extract PEP 508 Requirement objects from standard pip-style
requirements files.
"""

from pathlib import Path
from packaging.requirements import Requirement

from stalecheck.logger import setup_logger
from stalecheck.parsers.parser import Parser


class RequirementsTxtParser(Parser):
    """
    Parser implementation that handles requirements.txt files.

    This parser iterates over lines in a standard pip requirements file,
    ignoring comments and empty lines, and converts each valid line into
    a Requirement object.
    """

    def __init__(self, file: Path):
        self.logger = setup_logger(verbose=True)
        self.file: Path = file

    def get_packages(self) -> list[Requirement]:
        reqs = []
        with open(self.file, "r") as file_obj:
            for line in file_obj:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("-"):
                    self.logger.warning(f"Skipping pip flag/option: {line}")
                    continue

                try:
                    req = Requirement(line)
                    reqs.append(req)
                    self.logger.debug(
                        f"Parsed requirement: {req.name} ({req.specifier})"
                    )
                except Exception as e:
                    self.logger.error(f"Failed to parse line {line}: {str(e)}")

        return reqs


if __name__ == "__main__":
    test = RequirementsTxtParser(
        Path("/home/skovoroda/PycharmProjects/stalecheck/requirements.txt")
    )
    reqs = test.get_packages()
    for req in reqs:
        print(req.specifier[0].version)
