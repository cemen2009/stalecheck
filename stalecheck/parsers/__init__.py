from pathlib import Path
from typing import Union

from .requirements import RequirementsParser
from .pyproject import PyProjectParser
from .npm import NpmParser


parsers = {
    "requirements.txt": RequirementsParser,
    "pyproject.toml": PyProjectParser,
    "package.json": NpmParser,
}


def get_parser(file: Path) -> Union[RequirementsParser, PyProjectParser, NpmParser]:
    parser_cls = parsers.get(file.name)
    if parser_cls is None:
        raise ValueError(f"File {file} not supported")
    return parser_cls(file)
