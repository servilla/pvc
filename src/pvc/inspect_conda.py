#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Summary: Inspect a Conda environment file for a package and its version.

Module:
    inspect_conda

Author:
    servilla

Created:
    2026-01-24
"""
from pathlib import Path
import re

import daiquiri
import yaml


logger = daiquiri.getLogger(__name__)


def inspect(environment_file: Path, package_name: str) -> str | None:
    """Inspect a Conda environment.yml file for a package and its version.

    Args:
        environment_file (Path): Path to the Pixi lock file.
        package_name (str): Package name to inspect.

    Returns:
        str | None: Version of the package if found, otherwise None.
    """
    try:
        with open(environment_file, "r") as f:
            environment = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Error reading Pixi lock file: {e}")

    version = None
    for dependency in environment["dependencies"]:
        # Test for Conda package dependency
        if isinstance(dependency, str):
            if package_name in dependency:
                version = dependency.split("=")[1]
                break
        # Test for pip package dependency
        elif isinstance(dependency, dict) and "pip" in dependency:
            pip_dependencies = dependency["pip"]
            for pip_dependency in pip_dependencies:
                if package_name in pip_dependency:
                    version = pip_dependency.split("==")[1]
                    break

    return version
