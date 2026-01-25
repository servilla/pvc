#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Summary: Package version checker CLI for Python package managers.

Module:
    package_version_checker

Author:
    servilla

Created:
    2026-01-24
"""
import logging
from pathlib import Path
import sys

import click
import daiquiri


# Set up daiquiri logging: INFO and higher to LOGFILE, WARNING and higher to STDERR
CWD = Path(__file__).parent
LOGFILE = CWD / "package_version_checker.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.Stream(sys.stderr, level=logging.WARNING),
        daiquiri.output.File(LOGFILE, level=logging.INFO),
    ),
)
logger = daiquiri.getLogger(__name__)


VERSION = CWD / "VERSION.txt"

def print_version(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    print(f"pvc version: {VERSION.read_text("utf-8")}")
    ctx.exit()

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("package_name", required=True)
@click.option("--path", "-p", type=click.Path(exists=True), default=".", help="Path to project directory (default is all subdirectories from CWD.")
@click.option("--version", is_flag=True, default=False, callback=print_version, expose_value=False, is_eager=True, help="Output pvc version and exit.")
def pvc(package_name: str, path: str):
    """Package version checker CLI for Python package managers."""
    print (f"Checking {package_name} in {path}")
    return 0


if __name__ == "__main__":
    pvc()