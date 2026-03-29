from pathlib import Path
import tomlib

from packaging.requirements import Requirement

from stalecheck.logger import setup_logger
from stalecheck.parsers.parser import Parser


class PyProjectParser(Parser):
    def __init__(self, file: Path):
        self.logger = setup_logger(verbose=True)
        self.file: Path = file

    def get_packages(self) -> list[Requirement]:
        """
        Checking dependencies in pyproject.toml file.
        Assuming that pyproject.toml is using PEP 621 format or
        poetry tool-specific standard.
        """
        with open(self.file, "rb") as file_obj:
            data = tomlib.load(file_obj)
        
        reqs = []

        pep621_reqs = data.get("project", {}).get("dependencies", [])
        if pep621_reqs:
            self.logger.debug("PEP 621 requirements are listed in pyproject.toml")
            reqs += pep621_reqs        
        else:
            self.logger.debug("No PEP 621 requirements are listed in pyproject.toml")


        poetry_reqs = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
        if poetry_reqs:
            self.logger.debug("Poetry requirements are listed in pyproject.toml")

            for name, version in poetry_reqs.items():
                if name == "python":
                    continue

                # convert poetry dict format `pkg = version` to PEP 508 string `pkg==version`
                reqs.append(f"{name}=={version}" if isinstance(version, str) else name)
        else:
            self.logger.debug("No poetry requirements are listed in pyproject.toml")
        
        return [Requirement(req) for req in reqs]


parser = PyProjectParser(Path("/home/skovoroda/PycharmProjects/stalecheck/pyproject.toml"))
print(parser.get_packages())

