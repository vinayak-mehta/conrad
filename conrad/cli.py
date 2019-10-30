# -*- coding: utf-8 -*-

import os
import json
import hashlib
import datetime as dt
import random

import click
import requests
import sqlalchemy
from colorama import Fore, Style

from . import __version__, CONRAD_HOME, SQL_ALCHEMY_CONN
from .db import engine, Session
from .prettytable import PrettyTable
from .models import Base, Event, Reminder
from .utils import initialize_database, validate


def get_events():
    response = requests.get(
        "https://raw.githubusercontent.com/vinayak-mehta/conrad/master/data/events.json"
    )
    with open(os.path.join(CONRAD_HOME, "events.json"), "w") as f:
        f.write(json.dumps(response.json()))


def refresh_database(events):
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
            cfp_open=event["cfp_open"],
            cfp_start_date=dt.datetime.strptime(event["cfp_start_date"], "%Y-%m-%d"),
            cfp_end_date=dt.datetime.strptime(event["cfp_end_date"], "%Y-%m-%d"),
            start_date=dt.datetime.strptime(event["start_date"], "%Y-%m-%d"),
            end_date=dt.datetime.strptime(event["end_date"], "%Y-%m-%d"),
            source=event["source"],
            tags=event["tags"],
            kind=event["kind"],
        )
        session.add(e)
        session.commit()
    session.close()


@click.group(name="conrad")
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, *args, **kwargs):
    pass


@cli.command("refresh", short_help="Refresh event database")
@click.confirmation_option(prompt="Would you like conrad to look for new events?")
@click.pass_context
def _refresh(ctx, *args, **kwargs):
    if not os.path.exists(CONRAD_HOME):
        os.makedirs(CONRAD_HOME)

    get_events()
    if not os.path.exists(os.path.join(CONRAD_HOME, "conrad.db")):
        initialize_database()
    else:
        Event.__table__.drop(engine)
        Base.metadata.tables["event"].create(bind=engine)

    with open(os.path.join(CONRAD_HOME, "events.json"), "r") as f:
        events = json.load(f)
    refresh_database(events)

    # TODO: print("10 new events found!")
    click.echo("Event database updated!")


@cli.command("show", short_help="Show all saved events")
@click.option("--cfp", "-c", is_flag=True, help="Show only events which have an open Call For Proposals")
@click.option("--tag", "-t", default="", help="Look at conferences with a specific tag")
@click.option("--name", "-n", default="", help="Look at conferences containing a specific word in their name")
@click.option("--location", "-l", default="", help="Look at conferences in a specific city, state or country")
@click.option("--date", "-d", default=[], multiple=True, help="Look at conferences based on when they're happening. i.e conrad show --date \">= 2019-10-01\" --date \"<= 2020-01-01\"")
@click.pass_context
def _show(ctx, *args, **kwargs):
    # TODO: conrad show --new
    if not os.path.exists(CONRAD_HOME):
        os.makedirs(CONRAD_HOME)

    if not os.path.exists(os.path.join(CONRAD_HOME, "conrad.db")):
        click.echo("Event database not found, fetching it!")
        get_events()
        initialize_database()

        with open(os.path.join(CONRAD_HOME, "events.json"), "r") as f:
            events = json.load(f)
        refresh_database(events)

    cfp = kwargs["cfp"]
    tag = kwargs["tag"]
    name = kwargs["name"]
    date = list(kwargs["date"])
    location = kwargs["location"]

    filters = []
    if cfp:
        filters.append(Event.cfp_open.is_(cfp))
    if tag:
        filters.append(Event.tags.contains(tag))
    if name:
        filters.append(Event.name.ilike("%{}%".format(name)))
    if date:
        date_filters = []
        for d in date:
            cmp, date = d.split(" ")
            if not (">" in cmp or "<" in cmp):
                raise click.UsageError("Wrong comparison operator!")
            try:
                __ = dt.datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise click.UsageError("Wrong date format!")
            if ">" in cmp:
                date_filters.append(Event.start_date >= date)
            elif "<" in cmp:
                date_filters.append(Event.start_date <= date)
        filters.append(sqlalchemy.and_(*date_filters))
    if location:
        filters.append(
            sqlalchemy.or_(
                Event.city.ilike("%{}%".format(location)),
                Event.state.ilike("%{}%".format(location)),
                Event.country.ilike("%{}%".format(location)),
            )
        )

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
    events = list(
        session.query(Event).filter(*filters).order_by(Event.start_date).all()
    )
    if len(events):
        for event in events:
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
    else:
        click.echo("No events found!")


@cli.command("remind", short_help="Set and display reminders")
@click.option("--id", "-i", default=None, help="Conference identifier")
@click.pass_context
def _remind(ctx, *args, **kwargs):
    _id = kwargs["id"]
    t = PrettyTable()
    t.field_names = ["name", "start_date", "days_left", "fortune"]
    t.align = "l"

    fortunes = ["You should submit a proposal... There is still enough time!",
                "Believe in yourself and submit a proposal for this event. :)",
                "Take that step, submit a proposal and share your idea to the world!",
                "`Try not. Do or do not. There is no try` - Yoda",
                "What a nice day to submit a proposal to this event!"]

    if _id is None:
        session = Session()
        reminders = list(
            session.query(Event, Reminder)
            .filter(Event.id == Reminder.id)
            .order_by(Event.start_date)
            .all()
        )
        if len(reminders):
            for reminder, __ in reminders:
                start = dt.datetime.now()
                if reminder.cfp_open:
                    delta_days = (reminder.cfp_end_date - start).days
                    days_left = "{} days left to cfp deadline!".format(delta_days)
                else:
                    delta_days = (reminder.start_date - start).days
                    days_left = "{} days left!".format(delta_days)
                if delta_days > 30:
                    days_left = Fore.GREEN + Style.BRIGHT + days_left + Style.RESET_ALL
                elif delta_days < 30 and delta_days > 10:
                    days_left = Fore.YELLOW + Style.BRIGHT + days_left + Style.RESET_ALL
                elif delta_days < 10:
                    days_left = Fore.RED + Style.BRIGHT + days_left + Style.RESET_ALL
                t.add_row(
                    [reminder.name, reminder.start_date.strftime("%Y-%m-%d"), days_left, fortunes[random.randint(0, len(fortunes) - 1)]]
                )
            session.close()
            click.echo(t)
        else:
            click.echo("No reminders found!")
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


@cli.command("import", short_help="Import new events into conrad")
@click.option("--file", "-f", default=None, help="Json file to import")
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

    failures = validate(input_events)
    if len(failures):
        raise click.UsageError(
            "The following validations failed!\n{}".format(
                "".join(
                    list(map(lambda x: "- " + x + "\n", failures[:-1]))
                    + list(map(lambda x: "- " + x, failures[-1:]))
                )
            )
        )

    with open(EVENTS_PATH, "r") as f:
        events = json.load(f)

    new_events = []
    for ie in input_events:
        match = False
        for e in events:
            if (
                ie["name"].replace(" ", "").lower()
                in e["name"].replace(" ", "").lower()
            ):
                click.echo("Updating {}".format(e["name"]))
                e.update(ie)
                match = True
        if not match:
            new_events.append(ie)

    events.extend(new_events)
    click.echo("Added {} new events!".format(len(new_events)))
    with open(EVENTS_PATH, "w") as f:
        f.write(json.dumps(events, indent=4, sort_keys=True))
