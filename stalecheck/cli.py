from pathlib import Path

import click

from stalecheck.checker import Checker
from stalecheck.logger import setup_logger
from stalecheck.output import export_json, print_table


@click.command()
@click.option("--file", "-f", type=click.Path(exists=True))
@click.option("--export", type=click.Path())
@click.option("--verbose", "-v", is_flag=True)
def stalecheck(file, export, verbose):
    setup_logger(verbose)

    results = Checker().run(Path(file) if file else None)

    if export:
        export_json(results, Path(export))
    else:
        print_table(results)
