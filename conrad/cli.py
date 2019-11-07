# -*- coding: utf-8 -*-

import os
import re
import json
import hashlib
import datetime as dt

import click
import requests
import sqlalchemy
import textdistance
from colorama import Fore, Style
from cli_helpers import tabular_output

from . import __version__, CONRAD_HOME
from .db import engine, Session
from .models import Base, Event, Reminder
from .utils import initialize_database, validate


def set_default_pager():
    os_environ_pager = os.environ.get("PAGER")
    if os_environ_pager == "less":
        os.environ["LESS"] = "-SRXF"


def get_events():
    click.echo("Fetching latest events!")

    response = requests.get(
        "https://raw.githubusercontent.com/vinayak-mehta/conrad/master/data/events.json"
    )
    with open(os.path.join(CONRAD_HOME, "events.json"), "w") as f:
        f.write(json.dumps(response.json()))


def rebuild_events_table():
    with open(os.path.join(CONRAD_HOME, "events.json"), "r") as f:
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
            cfp_open=event["cfp_open"],
            cfp_end_date=dt.datetime.strptime(event["cfp_end_date"], "%Y-%m-%d"),
            start_date=dt.datetime.strptime(event["start_date"], "%Y-%m-%d"),
            end_date=dt.datetime.strptime(event["end_date"], "%Y-%m-%d"),
            source=event["source"],
            tags=event["tags"],
            kind=event["kind"],
            by=event["by"],
        )
        session.add(e)
        session.commit()
    session.close()


def initialize_conrad():
    conrad_update = os.path.join(CONRAD_HOME, ".conrad-update")
    if not os.path.exists(conrad_update):
        with open(conrad_update, "w") as f:
            f.write(dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

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


def update_conrad_update():
    conrad_update = os.path.join(CONRAD_HOME, ".conrad-update")
    with open(conrad_update, "w") as f:
        f.write(dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))


def clean_old_events():
    session = Session()

    now = dt.datetime.now()
    reminders = list(
        session.query(Event, Reminder)
        .filter(Event.id == Reminder.id, Event.cfp_end_date < now)
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
    conrad_update = os.path.join(CONRAD_HOME, ".conrad-update")
    if not os.path.exists(conrad_update):
        update_conrad_update()

    with open(conrad_update, "r") as f:
        last_update = dt.datetime.strptime(f.read().strip(), "%Y-%m-%dT%H:%M:%S")

    if (dt.datetime.now() - last_update) > dt.timedelta(days=1):
        refresh_conrad()
        clean_old_events()
        update_conrad_update()


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
    """conrad: Track conferences and meetups on your terminal!"""
    set_default_pager()


@bypass_auto_refresh
@cli.command("refresh", short_help="Refresh event database.")
@click.confirmation_option(prompt="Would you like conrad to look for new events?")
@click.pass_context
def _refresh(ctx, *args, **kwargs):
    # TODO: print("10 new events found!")
    refresh_conrad()

    click.echo("All done! ✨ 🍰 ✨")
    click.echo("Event database updated.")


@cli.command("show", short_help="Show all saved events.")
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

    session = Session()
    events = list(
        session.query(Event).filter(*filters).order_by(Event.start_date).all()
    )
    if len(events):
        header = [
            "id",
            "Name",
            "Website",
            "City",
            "State",
            "Country",
            "Start Date",
            "End Date",
        ]
        events_output = []

        for event in events:
            events_output.append(
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

        formatted = tabular_output.format_output(
            events_output, header, format_name="ascii"
        )
        click.echo_via_pager("\n".join(formatted))
    else:
        click.echo("No events found!")


@cli.command("remind", short_help="Set and display reminders.")
@click.option("--id", "-i", default=None, help="Conference identifier.")
@click.pass_context
def _remind(ctx, *args, **kwargs):
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
        if len(reminders):
            header = ["id", "Name", "Start Date", "Days Left"]
            reminders_output = []

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
                reminders_output.append(
                    [
                        reminder.id,
                        reminder.name,
                        reminder.start_date.strftime("%Y-%m-%d"),
                        days_left,
                    ]
                )
            session.close()

            formatted = tabular_output.format_output(
                reminders_output, header, format_name="ascii"
            )
            click.echo("\n".join(formatted))
        else:
            click.echo("No reminders found!")
    else:
        try:
            session = Session()
            if session.query(Event).filter(Event.id == _id).first() is None:
                click.echo("Event not found!")
            else:
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


@bypass_auto_refresh
@cli.command("import", short_help="Import new events into conrad.")
@click.option("--file", "-f", default=None, help="JSON file to import.")
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

    pattern = "[0-9]"
    new_events = []
    for ie in input_events:
        match = False
        for e in events:
            input_event_name = ie["name"].replace(" ", "").lower()
            input_event_name = re.sub(pattern, "", input_event_name)

            event_name = e["name"].replace(" ", "").lower()
            event_name = re.sub(pattern, "", event_name)

            similarity = textdistance.levenshtein.normalized_similarity(
                input_event_name, event_name
            )
            if similarity > 0.9:
                click.echo("Updating {}".format(e["name"]))
                e.update(ie)
                match = True
        if not match:
            click.echo("Adding {}".format(ie["name"]))
            new_events.append(ie)
    events.extend(new_events)

    s = "s" if len(new_events) > 1 else ""
    click.echo("Added {} new event{}!".format(len(new_events), s))
    with open(EVENTS_PATH, "w") as f:
        f.write(json.dumps(events, indent=4, sort_keys=True))
