# -*- coding: utf-8 -*-

import datetime as dt
import json
import logging
import os
import sys
from collections import Counter

import geopy.exc as geopyexceptions
import requests
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from packaging import version

from . import CONRAD_HOME, __version__
from .db import engine
from .schema import *

SELFCHECK_DATE_FMT = "%Y-%m-%dT%H:%M:%SZ"


logger = logging.getLogger(__name__)


# https://github.com/pypa/pip/blob/master/src/pip/_internal/self_outdated_check.py
class SelfCheckState(object):
    def __init__(self, cache_dir):
        self.state = {}
        self.statefile_path = os.path.join(cache_dir, "selfcheck.json")

        # Try to load the existing state
        try:
            with open(self.statefile_path, "r") as f:
                self.state = json.load(f)
        except (IOError, ValueError, KeyError, FileNotFoundError):
            # Explicitly suppressing exceptions, since we don't want to
            # error out if the cache file is invalid.
            pass

    def save(self, pypi_version, current_time):
        # If we do not have a path to cache in, don't bother saving.
        if not self.statefile_path:
            return

        state = {
            "last_check": current_time.strftime(SELFCHECK_DATE_FMT),
            "pypi_version": pypi_version,
        }

        text = json.dumps(state, sort_keys=True, separators=(",", ":"))

        with open(self.statefile_path, "w") as f:
            f.write(text)


def get_pypi_version():
    url = "https://pypi.org/pypi/conference-radar/json"
    response = requests.get(url)
    if response:
        data = response.json()
        pypi_version = data["info"]["version"]
        return pypi_version


def conrad_self_version_check():
    pypi_version = None

    try:
        state = SelfCheckState(cache_dir=CONRAD_HOME)

        current_time = dt.datetime.utcnow()
        # Determine if we need to refresh the state
        if "last_check" in state.state and "pypi_version" in state.state:
            last_check = dt.datetime.strptime(
                state.state["last_check"], SELFCHECK_DATE_FMT
            )
            if (current_time - last_check).total_seconds() < 7 * 24 * 60 * 60:
                pypi_version = state.state["pypi_version"]

        # Refresh the version if we need to or just see if we need to warn
        if pypi_version is None:
            pypi_version = get_pypi_version()

            # Save that we've performed a check
            state.save(pypi_version, current_time)

        conrad_version = version.parse(__version__)
        remote_version = version.parse(pypi_version)

        if conrad_version < remote_version:
            pip_cmd = "{} -m pip".format(sys.executable)
            logger.warning(
                f"You are using conrad version {__version__}; however,"
                f" version {pypi_version} is available.\n"
                "You should consider upgrading with"
                f" '{pip_cmd} install --upgrade conference-radar'."
            )
    except Exception:
        logger.debug(
            "There was an error checking the latest version of conrad",
            exc_info=True,
        )


def initialize_database():
    from .models import Base

    Base.metadata.create_all(engine)


def reset_database():
    from .models import Base

    Base.metadata.drop_all(engine)
    initialize_database()


def get_address(place):
    geolocator = Nominatim(user_agent="conrad")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)

    address = None
    try:
        location = geolocator.geocode(place)
        if location is not None:
            address = geolocator.reverse(
                "{lat}, {lon}".format(lat=location.latitude, lon=location.longitude)
            ).raw["address"]
            address["latitude"] = location.latitude
            address["longitude"] = location.longitude
    except geopyexceptions.GeocoderTimedOut:
        # TODO: add 2 retries using tenacity
        print(f"Geocoder timed out for {place}!")

    return address


def apply_schema(events, version=LATEST):
    schema = eval(f"v{version}")
    _events = []

    for event in events:
        _event = dict({k: v for k, v in event.items() if k in schema.keys()})
        _events.append(_event)

    return _events


def validate_events(input_events, version=LATEST):
    schema = eval(f"v{version}")
    failures = []

    # check for duplicates (name + start_date to allow same conference in different years)
    ie_identifiers = [
        (ie["name"].replace(" ", "").lower(), ie["start_date"]) for ie in input_events
    ]
    duplicate_events = [
        event for event, count in Counter(ie_identifiers).items() if count > 1
    ]
    if duplicate_events:
        failures.append(f"Duplicate events found: {duplicate_events}")

    # check if keys exist
    for ie in input_events:
        if set(schema.keys()).difference(set(ie.keys())):
            failures.append("Required fields not found")
            break

    return failures


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
