# -*- coding: utf-8 -*-

import datetime as dt
import hashlib
import inspect
import json
import os
import re
import shutil
import sys

import click
import requests
import sqlalchemy
import textdistance
from rich.console import Console
from rich.table import Table

try:
    import bs4
    import cerberus
    import git
    import googleapiclient
    import pandas
except ImportError:
    _HAS_CRAWL_REQUIREMENTS = False
else:
    _HAS_CRAWL_REQUIREMENTS = True

if _HAS_CRAWL_REQUIREMENTS:
    import crawlers
    from crawlers import *

from . import CONRAD_HOME, __version__
from .db import Session, engine
from .models import Base, Event, Reminder
from .schema import *
from .utils import apply_schema, initialize_database, mkdir, validate_events

DATE_FMT = "%Y-%m-%dT%H:%M:%S"


def has_less():
    return shutil.which("less")


def set_default_pager():
    if has_less() is not None:
        os.environ["LESS"] = "-SRXF"


def get_events():
    click.echo("Fetching latest events.")

    events_filename = eval(f"f{LATEST}")
    response = requests.get(
        f"https://raw.githubusercontent.com/vinayak-mehta/conrad/master/data/{events_filename}",
        timeout=5,
    )
    with open(os.path.join(CONRAD_HOME, events_filename), "w") as f:
        f.write(json.dumps(response.json()))


def rebuild_events_table():
    events_filename = eval(f"f{LATEST}")
    with open(os.path.join(CONRAD_HOME, events_filename), "r") as f:
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
            location=event["location"],
            cfp_open=event["cfp_open"],
            cfp_end_date=dt.datetime.strptime(event["cfp_end_date"], "%Y-%m-%d"),
            start_date=dt.datetime.strptime(event["start_date"], "%Y-%m-%d"),
            end_date=dt.datetime.strptime(event["end_date"], "%Y-%m-%d"),
            source=event["source"],
            tags=json.dumps(event["tags"]),
            kind=event["kind"],
            by=event["by"],
        )
        session.add(e)
        session.commit()
    session.close()


def set_update_timestamp(overwrite=False):
    updated_at = os.path.join(CONRAD_HOME, ".updated_at")
    if overwrite or not os.path.exists(updated_at):
        with open(updated_at, "w") as f:
            f.write(dt.datetime.now().strftime(DATE_FMT))


def initialize_conrad():
    set_update_timestamp()

    if not os.path.exists(os.path.join(CONRAD_HOME, "conrad.db")):
        get_events()
        initialize_database()
        rebuild_events_table()


def refresh_conrad():
    get_events()
    if not os.path.exists(os.path.join(CONRAD_HOME, "conrad.db")):
        initialize_database()
    else:
        Event.__table__.drop(engine)
        Base.metadata.tables["event"].create(bind=engine)
    rebuild_events_table()
    set_update_timestamp(overwrite=True)


def clean_old_events():
    session = Session()

    now = dt.datetime.now()
    reminders = list(
        session.query(Event, Reminder)
        .filter(Event.id == Reminder.id, Event.end_date < now)
        .all()
    )
    for r, __ in reminders:
        session.query(Reminder).filter(Reminder.id == r.id).delete()

    events = list(session.query(Event).filter(Event.end_date < now).all())
    for e in events:
        session.query(Event).filter(Event.id == e.id).delete()

    session.commit()
    session.close()


def auto_refresh():
    try:
        updated_at = os.path.join(CONRAD_HOME, ".updated_at")
        with open(updated_at, "r") as f:
            last_updated_at = dt.datetime.strptime(f.read().strip(), DATE_FMT)
    except (IOError, FileNotFoundError):
        last_updated_at = dt.datetime.strptime("1970-01-01T00:00:00", DATE_FMT)

    if (dt.datetime.now() - last_updated_at) > dt.timedelta(days=7):
        refresh_conrad()
        clean_old_events()


# https://stackoverflow.com/a/50889894
def make_exclude_hook_command(callback):
    """for any command that is not decorated, call the callback"""
    hook_attr_name = "hook_" + callback.__name__

    class HookGroup(click.Group):
        """group to hook context invoke to see if the callback is needed"""

        def group(self, *args, **kwargs):
            """new group decorator to make sure sub groups are also hooked"""
            if "cls" not in kwargs:
                kwargs["cls"] = type(self)
            return super(HookGroup, self).group(*args, **kwargs)

        def command(self, *args, **kwargs):
            """new command decorator to monkey patch command invoke"""

            cmd = super(HookGroup, self).command(*args, **kwargs)

            def hook_command_decorate(f):
                # decorate the command
                ret = cmd(f)

                # grab the original command invoke
                orig_invoke = ret.invoke

                def invoke(ctx):
                    """call the call back right before command invoke"""
                    parent = ctx.parent
                    sub_cmd = (
                        parent and parent.command.commands[parent.invoked_subcommand]
                    )
                    if (
                        not sub_cmd
                        or not isinstance(sub_cmd, click.Group)
                        and getattr(sub_cmd, hook_attr_name, True)
                    ):
                        # invoke the callback
                        callback()
                    return orig_invoke(ctx)

                # hook our command invoke to command and return cmd
                ret.invoke = invoke
                return ret

            # return hooked command decorator
            return hook_command_decorate

    def decorator(func=None):
        if func is None:
            # if called other than as decorator, return group class
            return HookGroup

        setattr(func, hook_attr_name, False)

    return decorator


bypass_auto_refresh = make_exclude_hook_command(auto_refresh)


@click.group(name="conrad", cls=bypass_auto_refresh())
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, *args, **kwargs):
    """conrad: Track conferences and meetups on your terminal."""
    set_default_pager()


@bypass_auto_refresh
@cli.command("refresh", short_help="Refresh event database.")
@click.confirmation_option(prompt="Would you like conrad to look for new events?")
@click.pass_context
def _refresh(ctx, *args, **kwargs):
    # TODO: print("10 new events found.")
    refresh_conrad()

    click.echo("All done! ✨ 🍰 ✨")
    click.echo("Event database updated.")


@cli.command("show", short_help="Show all saved events.")
@click.option(
    "--id",
    "-i",
    help="Show event with a particular id.",
)
@click.option(
    "--kind",
    "-k",
    help="Show kind of event, conference or meetup.",
)
@click.option(
    "--cfp",
    "-c",
    is_flag=True,
    help="Show only events which have an open CFP (call for proposals).",
)
@click.option(
    "--tag", "-t", default="", help="Look at conferences with a specific tag."
)
@click.option(
    "--name",
    "-n",
    default="",
    help="Look at conferences containing a specific word in their name.",
)
@click.option(
    "--location",
    "-l",
    default="",
    help="Look at conferences in a specific city, state or country.",
)
@click.option(
    "--date",
    "-d",
    default=[],
    multiple=True,
    help='Look at conferences based on when they\'re happening. For example: conrad show --date ">= 2019-10-01" --date "<= 2020-01-01".',
)
@click.pass_context
def _show(ctx, *args, **kwargs):
    # TODO: conrad show --new
    initialize_conrad()

    _id = kwargs["id"]
    kind = kwargs["kind"]
    cfp = kwargs["cfp"]
    tag = kwargs["tag"]
    name = kwargs["name"]
    date = list(kwargs["date"])
    location = kwargs["location"]

    filters = []
    if _id:
        filters.append(Event.id == _id)
    if kind:
        filters.append(Event.kind == kind)
    if cfp:
        filters.append(Event.cfp_open.is_(cfp))
    if tag:
        filters.append(Event.tags.contains(tag))
    if name:
        filters.append(Event.name.ilike(f"%{name}%"))
    if date:
        date_filters = []
        for d in date:
            cmp, date = d.split(" ")
            if not (">" in cmp or "<" in cmp):
                raise click.UsageError("Wrong comparison operator.")
            try:
                __ = dt.datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise click.UsageError("Wrong date format.")
            if ">" in cmp:
                date_filters.append(Event.start_date >= date)
            elif "<" in cmp:
                date_filters.append(Event.start_date <= date)
        filters.append(sqlalchemy.and_(*date_filters))
    if location:
        filters.append(
            sqlalchemy.or_(
                Event.name.ilike(f"%{location}%"),
                Event.city.ilike(f"%{location}%"),
                Event.state.ilike(f"%{location}%"),
                Event.country.ilike(f"%{location}%"),
                Event.location.ilike(f"%{location}%"),
            )
        )

    session = Session()
    try:
        events = list(
            session.query(Event).filter(*filters).order_by(Event.start_date).all()
        )
    except sqlalchemy.exc.OperationalError:
        refresh_conrad()
        events = list(
            session.query(Event).filter(*filters).order_by(Event.start_date).all()
        )

    if len(events) > 0:
        console = Console()
        table = Table(show_header=True, header_style="bold magenta", show_lines=True)

        table.add_column("id")
        table.add_column("Name")
        table.add_column("Website")
        table.add_column("City")
        table.add_column("Country")
        table.add_column("Start Date")
        table.add_column("End Date")

        events_output = []

        rids = [r.id for r in session.query(Reminder).all()]
        for event in events:
            event_output = [
                event.id,
                event.name,
                event.url,
                event.city,
                event.country,
                event.start_date.strftime("%Y-%m-%d"),
                event.end_date.strftime("%Y-%m-%d"),
            ]

            # highlight event which has a reminder set
            if event.id in rids:
                event_output = list(
                    map(
                        lambda x: f"[bold][green]{x}[/green][/bold]",
                        event_output,
                    )
                )

            table.add_row(*event_output)

        session.close()

        console_kwargs = {}
        if has_less():
            console_kwargs["styles"] = True

        with console.pager(**console_kwargs):
            console.print(table)
    else:
        click.echo("No events found.")


@cli.command("remind", short_help="Set and display reminders.")
@click.option("--id", "-i", default=None, help="Conference identifier.")
@click.pass_context
def _remind(ctx, *args, **kwargs):
    def get_days_left(event):
        start = dt.datetime.now()
        cfp_days_left = (event.cfp_end_date - start).days
        event_days_left = (event.start_date - start).days

        if event.cfp_open and cfp_days_left >= 0:
            days_left = cfp_days_left
        elif event_days_left >= 0:
            days_left = event_days_left
        else:
            days_left = -1

        return days_left, event.cfp_open

    initialize_conrad()

    _id = kwargs["id"]

    if _id is None:
        session = Session()
        reminders = list(
            session.query(Event, Reminder)
            .filter(Event.id == Reminder.id)
            .order_by(Event.start_date)
            .all()
        )
        if len(reminders) > 0:
            console = Console()
            table = Table(
                show_header=True, header_style="bold magenta", show_lines=True
            )

            table.add_column("id")
            table.add_column("Name")
            table.add_column("Start Date")
            table.add_column("Days Left")

            for reminder, __ in reminders:
                days_left, cfp_open = get_days_left(reminder)

                if cfp_open and days_left >= 0:
                    days_left_output = f"{days_left} days left to cfp deadline"
                elif days_left >= 0:
                    days_left_output = f"{days_left} days left"
                else:
                    days_left_output = "Event ended"

                style = "white"
                if days_left >= 30:
                    style = "green"
                elif 30 > days_left >= 10:
                    style = "yellow"
                elif 10 > days_left >= 0:
                    style = "red"

                days_left_output = f"[bold][{style}]{days_left_output}[/{style}][/bold]"
                reminder_output = [
                    reminder.id,
                    reminder.name,
                    reminder.start_date.strftime("%Y-%m-%d"),
                    days_left_output,
                ]

                table.add_row(*reminder_output)

            session.close()

            console_kwargs = {}
            if has_less():
                console_kwargs["styles"] = True

            with console.pager(**console_kwargs):
                console.print(table)
        else:
            click.echo("No reminders found.")
    else:
        try:
            session = Session()
            event = session.query(Event).filter(Event.id == _id).first()
            if event is None:
                click.echo("Event not found.")
            else:
                days_left, __ = get_days_left(event)

                if days_left == -1:
                    click.echo("Event ended.")
                else:
                    reminder = Reminder(id=event.id)
                    session.add(reminder)
                    session.commit()
                    session.close()

                    click.echo("Reminder set.")
        except sqlalchemy.exc.IntegrityError:
            session.rollback()

            if click.confirm("Do you want to remove this reminder?"):
                session = Session()
                session.query(Reminder).filter(Reminder.id == _id).delete()
                session.commit()
                session.close()

                click.echo("Reminder removed.")


@cli.command("generate", short_help="Generate skeleton crawler code.")
@click.argument("entity")
@click.argument("entity_name")
@click.pass_context
def _generate(ctx, *args, **kwargs):
    SUPPORTED_ENTITIES = ["crawler"]

    entity = kwargs["entity"]

    if entity not in SUPPORTED_ENTITIES:
        click.UsageError(f"Entity '{entity}' not supported")

    entity_name = kwargs["entity_name"]
    entity_name_snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", entity_name).lower()

    crawler_dir = f"crawlers/{entity_name_snake_case}"
    mkdir(crawler_dir)

    with open(os.path.join(crawler_dir, "__init__.py"), "w") as f:
        f.write("# -*- coding: utf-8 -*-\n")

    crawler_content = f"""# -*- coding: utf-8 -*-

from ..base import BaseCrawler


class {entity_name}Crawler(BaseCrawler):
    def get_events(self):
        # Populate this list of events using your code
        events = []

        # YOUR CODE HERE

        # Extend the self.events list with the new list
        self.events.extend(events)
"""

    crawler_path = os.path.join(crawler_dir, f"{entity_name_snake_case}_crawler.py")
    with open(crawler_path, "w") as f:
        f.write(crawler_content)

    with open("crawlers/__init__.py", "a") as f:
        f.write(
            f"from .{entity_name_snake_case}.{entity_name_snake_case}_crawler import {entity_name}Crawler"
        )

    click.echo(f"\t{click.style('create', fg='green', bold=True)}\t{crawler_path}")


@cli.command("run", short_help="Run crawler code.")
@click.argument("entity")
@click.argument("entity_name")
@click.pass_context
def _run(ctx, *args, **kwargs):
    if not _HAS_CRAWL_REQUIREMENTS:
        raise click.UsageError(
            "To run crawlers, please install the requirements with\n"
            "'pip install --upgrade conference-radar[crawl]'."
        )

    SUPPORTED_ENTITIES = ["crawler"]

    entity = kwargs["entity"]

    if entity not in SUPPORTED_ENTITIES:
        click.UsageError(f"Entity '{entity}' not supported")

    entity_name = kwargs["entity_name"]
    entity_name_snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", entity_name).lower()

    crawler = [
        m[0]
        for m in inspect.getmembers(crawlers, inspect.isclass)
        if m[1].__module__.startswith("crawlers") and m[0] == f"{entity_name}Crawler"
    ]
    if len(crawler):
        filename = crawler[0].lower().replace("crawler", "")

        Crawler = eval(crawler[0])
        c = Crawler()
        c.get_events()

        crawler_data_path = f"data/{filename}.json"
        c.export(crawler_data_path)

        click.echo(
            f"\t{click.style('save', fg='green', bold=True)}\t{crawler_data_path}"
        )
    else:
        print("Crawler not found.")


@bypass_auto_refresh
@cli.command("import", short_help="Import new events into conrad.")
@click.option("--file", "-f", default=None, help="JSON file to import.")
@click.pass_context
def _import(ctx, *args, **kwargs):
    file = kwargs["file"]

    if file is None:
        raise click.UsageError("No file provided.")

    if not os.path.exists(file):
        raise click.UsageError("File does not exist.")

    with open(file, "r") as f:
        input_events = json.load(f)

    failures = validate_events(input_events, version=LATEST)
    if len(failures) > 0:
        raise click.UsageError(
            "The following validations failed!\n{}".format(
                "".join(
                    list(map(lambda x: "- " + x + "\n", failures[:-1]))
                    + list(map(lambda x: "- " + x, failures[-1:]))
                )
            )
        )

    events_path = os.path.join(os.getcwd(), "data", f"{eval(f'f{LATEST}')}")
    try:
        with open(events_path, "r") as f:
            events = json.load(f)
    except (IOError, ValueError, KeyError, FileNotFoundError):
        events = []

    now = dt.datetime.now()
    old_events = []
    for e in events:
        event_end_date = dt.datetime.strptime(e["end_date"], "%Y-%m-%d")
        if event_end_date < now:
            print(f"Removing {e['name']}")
            continue

        if e["cfp_end_date"] is not None:
            cfp_end_date = dt.datetime.strptime(e["cfp_end_date"], "%Y-%m-%d")
            if cfp_end_date < now:
                e["cfp_open"] = False

        old_events.append(e)

    removed = len(events) - len(old_events)
    s = "s" if removed != 1 else ""
    click.echo(f"Removed {removed} old event{s}.")

    pattern = "[0-9]"
    new_events = []
    for ie in input_events:
        if ie["end_date"] is None:
            continue

        event_end_date = dt.datetime.strptime(ie["end_date"], "%Y-%m-%d")
        if event_end_date < now:
            continue

        if ie["cfp_end_date"] is not None:
            cfp_end_date = dt.datetime.strptime(ie["cfp_end_date"], "%Y-%m-%d")
            if cfp_end_date < now:
                ie["cfp_open"] = False

        match = False
        for oe in old_events:
            input_event_name = ie["name"].replace(" ", "").lower()
            input_event_name = re.sub(pattern, "", input_event_name)

            old_event_name = oe["name"].replace(" ", "").lower()
            old_event_name = re.sub(pattern, "", old_event_name)

            similarity = textdistance.levenshtein.normalized_similarity(
                input_event_name, old_event_name
            )
            if similarity > 0.9:
                click.echo(f"Updating {oe['name']}")
                oe.update(ie)
                match = True
        if not match:
            click.echo(f"Adding {ie['name']}")
            new_events.append(ie)
    old_events.extend(new_events)

    s = "s" if len(new_events) != 1 else ""
    click.echo(f"Added {len(new_events)} new event{s}.")
    with open(events_path, "w") as f:
        f.write(json.dumps(old_events, indent=4, sort_keys=True))

    for version in reversed(range(1, int(LATEST))):
        events = old_events.copy()
        events = apply_schema(events, version=version)

        events_path = os.path.join(os.getcwd(), "data", f"{eval(f'f{version}')}")
        with open(events_path, "w") as f:
            f.write(json.dumps(events, indent=4, sort_keys=True))
