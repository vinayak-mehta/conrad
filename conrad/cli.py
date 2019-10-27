# -*- coding: utf-8 -*-

import os

import git
import click

from . import __version__, CONRAD_HOME
from .prettytable import PrettyTable


@click.group(name="conrad")
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, *args, **kwargs):
    pass


@cli.command("refresh")
@click.pass_context
def _refresh(ctx, *args, **kwargs):
    if not os.path.exists(CONRAD_HOME):
        os.makedirs(CONRAD_HOME)
        git.Repo.clone_from("https://github.com/vinayak-mehta/conrad", CONRAD_HOME)
    else:
        g = git.cmd.Git(CONRAD_HOME)
        g.pull()


@cli.command("show")
@click.pass_context
def _show(ctx, *args, **kwargs):
    pass


@cli.command("remind")
@click.pass_context
def _remind(ctx, *args, **kwargs):
    pass


@cli.command("import")
@click.pass_context
def _import(ctx, *args, **kwargs):
    pass
