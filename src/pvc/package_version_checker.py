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

import pvc.inspect_pixi as inspect_pixi
import pvc.inspect_conda as inspect_conda


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

CONDA = "environment.yml"
PIXI = "pixi.lock"

VERSION = CWD / "VERSION.txt"


def seek_env(path: Path, package_name: str, verbose: int) -> None:
    conda = pixi = None
    if (path / CONDA).exists():
        conda = path / CONDA
        version = inspect_conda.inspect(conda, package_name)
        project_name = conda.parent.name if verbose == 0 else conda
        if version is not None: click.echo(f"{package_name}-{version}  {project_name}")
    if (path / PIXI).exists():
        pixi = path / PIXI
        version = inspect_pixi.inspect(pixi, package_name)
        project_name = pixi.parent.name if verbose == 0 else pixi
        if version is not None: click.echo(f"{package_name}-{version}  {project_name}")


    if verbose > 1 and (conda is None and pixi is None):
        print(f"Neither a {CONDA} or a {PIXI} file were found in {path}.")


def print_version(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    print(f"pvc version: {VERSION.read_text("utf-8")}")
    ctx.exit()

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("package", required=True)
@click.option("--path", "-p", type=click.Path(exists=True), default=None, help="Path to project directory (default is all subdirectories from CWD.")
@click.option("--verbose", "-v", count=True, default=False, help="Increase verbosity level.")
@click.option("--version", is_flag=True, default=False, callback=print_version, expose_value=False, is_eager=True, help="Output pvc version and exit.")
def pvc(package: str, path: str, verbose: int):
    """
    Package version checker (PVC) CLI for Python package managers.\n

    PVC will check the CWD and all subdirectories for a Python environment
    from the CWD to a depth of n=1 below the CWD, looking for either a
    Conda environment.yml file or a Pixi lock (pixi.lock) file to identify
    the package of interest. If a path option is provided, PVC will
    check only the specified directory at depth n=0. If the package
    is found, PVC will display the directory name in which the environment
    file was found and the version number of the package.

    """

    if path is None:
        # Check CWD and all subdirectories from CWD to a depth of n=1
        cwd = Path.cwd()
        seek_env(cwd, package, verbose)
        for p in cwd.iterdir():
            if p.is_dir(): seek_env(p, package, verbose)
    else:
        # Check only the specified directory to a depth of n=0
        p = Path(path).resolve()
        if p.is_dir(): seek_env(p, package, verbose)

    return 0


if __name__ == "__main__":
    pvc()