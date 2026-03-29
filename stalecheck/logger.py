import logging
import sys


def setup_logger(verbose: bool = False) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO

    logger = logging.getLogger("stalecheck")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s - [%(levelname)s] - %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
    else:
        # If the level was changed during a second call, update it.
        logger.handlers[0].setLevel(level)

    return logger
