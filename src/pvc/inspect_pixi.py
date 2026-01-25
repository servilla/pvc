#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Summary: Inspect a Pixi lock file for a package and its version.

Module:
    inspect_pixi

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


def inspect(pixi_lock_file: Path, package_name: str) -> str | None:
    """Inspect a Pixi lock file for a package and its version.

    Args:
        pixi_lock_file (Path): Path to the Pixi lock file.
        package_name (str): Package name to inspect.

    Returns:
        str | None: Version of the package if found, otherwise None.
    """
    try:
        with open(pixi_lock_file, "r") as f:
            pixi_lock = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Error reading Pixi lock file: {e}")

    version = None
    for package in pixi_lock["packages"]:
        if "conda" in package:
            key = "conda"
        elif "pypi" in package:
            key = "name"
        else:
            key = None
        if key is not None and package_name in package[key]:
            version = ""
            if key == "conda":
                pattern = rf"{package_name}-([^-]+)-"
                match = re.search(pattern, package[key])
                if match: version = match.group(1)
            else: # key == "name" - pypi
                if "version" in package: version = package["version"]

    return version
