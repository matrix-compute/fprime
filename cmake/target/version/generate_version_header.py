#!/usr/bin/env python3
"""
# ===============================================================================
# NAME: generate_version_header.py
#
# DESCRIPTION:  Creates a version header file of specified name.
#               It takes as input a filename and creates a header file
#               with a constant string which is the git hash of the current version
#
# USAGE: ./generate_version_header.py /path/tofile/version.hpp
#
# AUTHOR: sfregoso
# EMAIL:  sfregoso@jpl.nasa.gov
# DATE CREATED  : Oct. 15, 2021
#
# Copyright 2021, California Institute of Technology.
# ALL RIGHTS RESERVED. U.S. Government Sponsorship acknowledged.
# ===============================================================================
"""
import sys
import os
import argparse

from fprime_ac.utils.version import (
    get_fprime_version,
    get_project_version,
    FALLBACK_VERSION,
)


def create_version_file(fid, framework_version, project_version):
    """
    Create the version file using the provided name and path.
    """
    # Open file for writing
    fid.write("/*\n")
    fid.write(
        "    This file has been autogenerated using [{}].\n".format(
            os.path.basename(__file__)
        )
    )
    fid.write("    This file may be overwritten.\n")
    fid.write("*/\n")
    fid.write("#ifndef _VERSION_HPP_\n")
    fid.write("#define _VERSION_HPP_\n")
    fid.write("\n")
    fid.write(
        'static const char* FRAMEWORK_VERSION = "{}";\n'.format(framework_version)
    )
    fid.write('static const char* PROJECT_VERSION = "{}";\n'.format(framework_version))
    fid.write("\n")
    fid.write("#endif\n")
    fid.write("\n")


def main():
    """
    Main program entry point
    """
    parser = argparse.ArgumentParser(description="Create version header")
    parser.add_argument(
        "output",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Path to write version header into",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Check framework and fallback version",
    )
    args = parser.parse_args()

    # Build the version output
    fprime_version = get_fprime_version()
    project_version = get_project_version()
    create_version_file(args.output, fprime_version, project_version)

    # Check version if asked to do so
    if args.check and not fprime_version.startswith(FALLBACK_VERSION):
        expected = fprime_version[: len(FALLBACK_VERSION)]
        print(
            f"[ERROR] Fallback version { FALLBACK_VERSION } not updated. Expected { expected }.",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
