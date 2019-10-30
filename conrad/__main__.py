# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __version__ import __version__
from setuptools.version import pkg_resources
import requests
import logging

__all__ = ("main",)


def main():
    from conrad.cli import cli

    cli()


def get_current_version():

    url = "https://pypi.org/pypi/conference-radar/json"
    response = requests.get(url)
    if response:
        data = response.json()
        current_version = data["info"]["version"]
        return current_version
    return ""


def conrad_self_version_check():

    current_version = get_current_version()
    logger = logging.getLogger(__name__)
    if current_version:
        if pkg_resources.parse_version(__version__) <\
                pkg_resources.parse_version(current_version):
            logger.warning("You are using conrad version %s; however,"
                           " version %s is available.\n"
                           "You should consider upgrading via the "
                           "'pip install --upgrade conference-radar' command.\n",
                           __version__, current_version)


if __name__ == "__main__":

    conrad_self_version_check()
    main()
