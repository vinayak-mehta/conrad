# -*- coding: utf-8 -*-

from .utils import conrad_self_version_check


__all__ = ("main",)


def main():
    from conrad.cli import cli

    conrad_self_version_check()
    cli()


if __name__ == "__main__":
    main()
