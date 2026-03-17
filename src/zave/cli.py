"""Main CLI entry point for zave."""

import click
from zave.commands import init


@click.group()
@click.version_option(version="0.1.0", prog_name="zave")
def cli():
    """ZaveStudios platform workload generator.

    Generate platform-compliant workload repositories from contracts.
    """
    pass


cli.add_command(init.init)


if __name__ == "__main__":
    cli()
