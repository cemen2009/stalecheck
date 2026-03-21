import logging
import sys


def setup_logger(verbose: bool = False) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO

    logger = logging.getLogger("stalecheck")
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)

    formatter = logging.Formatter(
        # check both and delete inappropriate
        # fmt="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        fmt="%(asctime)s - [%(levelname)s] - %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
