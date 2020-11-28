# -*- coding: utf-8 -*-

from .utils import conrad_self_version_check
from conrad.cli import cli


__all__ = ("main",)


def main():
    conrad_self_version_check()
    cli()


if __name__ == "__main__":
    main()
