from stalecheck.parsers.parser import Parser


class PyProjectParser(Parser):
    def __init__(self, file: Path):
        self.logger = setup_logger(verbose=True)
        self.file: Path = file

    def get_packages(self) -> list[Requirement]:
        ...