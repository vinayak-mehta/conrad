# -*- coding: utf-8 -*-

import os
import json
import hashlib
import datetime as dt

import git
import click
import sqlalchemy
from colorama import Fore, Style

from . import __version__, CONRAD_HOME, SQL_ALCHEMY_CONN
from .db import engine, Session
from .prettytable import PrettyTable
from .models import Base, Event, Reminder
from .utils import initialize_database, validate_import


@click.group(name="conrad")
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, *args, **kwargs):
    pass


@cli.command("refresh")
@click.confirmation_option(prompt="Would you like conrad to look for new events?")
@click.pass_context
def _refresh(ctx, *args, **kwargs):
    if not os.path.exists(CONRAD_HOME):
        os.makedirs(CONRAD_HOME)
        git.Repo.clone_from("https://github.com/vinayak-mehta/conrad", CONRAD_HOME)
    else:
        g = git.cmd.Git(CONRAD_HOME)
        g.pull()

    if not os.path.exists(os.path.join(CONRAD_HOME, "conrad.db")):
        initialize_database()
    else:
        Event.__table__.drop(engine)
        Base.metadata.tables["event"].create(bind=engine)

    with open(os.path.join(CONRAD_HOME, "data/events.json"), "r") as f:
        events = json.load(f)

    session = Session()
    for event in events:
        event_id = hashlib.md5(
            (event["name"] + event["start_date"]).encode("utf-8")
        ).hexdigest()
        e = Event(
            id=event_id[:6],
            name=event["name"],
            url=event["url"],
            city=event["city"],
            state=event["state"],
            country=event["country"],
            start_date=dt.datetime.strptime(event["start_date"], "%Y-%m-%d"),
            end_date=dt.datetime.strptime(event["end_date"], "%Y-%m-%d"),
            source=event["source"],
            tags=event["tags"],
            kind=event["kind"],
        )
        session.add(e)
        session.commit()
    session.close()

    # TODO: print("10 new events found!")
    click.echo("Event database updated!")


@cli.command("show")
@click.pass_context
def _show(ctx, *args, **kwargs):
    # TODO: conrad show -c
    # TODO: conrad show -t python
    # TODO: conrad show -l city/country
    # TODO: conrad show -d >= 2019-08-01 AND <= 2019-10-01

    t = PrettyTable()
    t.field_names = [
        "id",
        "name",
        "url",
        "city",
        "state",
        "country",
        "start_date",
        "end_date",
    ]
    t.align = "l"

    session = Session()
    for event in session.query(Event).order_by(Event.start_date).all():
        t.add_row(
            [
                event.id,
                event.name,
                event.url,
                event.city,
                event.state,
                event.country,
                event.start_date.strftime("%Y-%m-%d"),
                event.end_date.strftime("%Y-%m-%d"),
            ]
        )
    session.close()

    click.echo(t)


@cli.command("remind")
@click.option("--id", "-i", default=None)
@click.pass_context
def _remind(ctx, *args, **kwargs):
    _id = kwargs["id"]
    t = PrettyTable()
    t.field_names = ["name", "start_date", "time_left"]

    if _id is None:
        session = Session()
        reminders = (
            session.query(Event, Reminder)
            .filter(Event.id == Reminder.id)
            .order_by(Event.start_date)
            .all()
        )
        for reminder, __ in reminders:
            t.add_row(
                [
                    reminder.name,
                    reminder.start_date.strftime("%Y-%m-%d"),
                    Fore.RED + Style.BRIGHT + "10 days left!" + Style.RESET_ALL,
                ]
            )
        session.close()

        click.echo(t)
    else:
        try:
            session = Session()
            reminder = Reminder(id=_id)
            session.add(reminder)
            session.commit()
            session.close()

            click.echo("Reminder set!")
        except sqlalchemy.exc.IntegrityError:
            session.rollback()

            if click.confirm("Do you want to remove this reminder?"):
                session = Session()
                session.query(Reminder).filter(Reminder.id == _id).delete()
                session.commit()
                session.close()

                click.echo("Reminder removed!")


@cli.command("import")
@click.option("--file", "-f", default=None)
@click.pass_context
def _import(ctx, *args, **kwargs):
    file = kwargs["file"]
    EVENTS_PATH = os.path.join(os.getcwd(), "data", "events.json")

    if file is None:
        raise click.UsageError("No file provided!")
    if not os.path.exists(file):
        raise click.UsageError("File does not exist!")

    with open(file, "r") as f:
        input_events = json.load(f)

    with open(EVENTS_PATH, "r") as f:
        events = json.load(f)

    new_events = []
    for ie in input_events:
        for e in events:
            if (
                ie["name"].replace(" ", "").lower()
                in e["name"].replace(" ", "").lower()
            ):
                click.echo("Updating {}".format(e["name"]))
                e.update(ie)
            else:
                new_events.append(ie)

    events.extend(new_events)
    with open(EVENTS_PATH, "w") as f:
        f.write(json.dumps(events, indent=4, sort_keys=True))
