import click


@click.group()
@click.pass_context
def stalecheck(ctx):
    """
    Test help
    """
    ctx.obj = ...
