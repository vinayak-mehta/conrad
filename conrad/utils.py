# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import datetime as dt
from setuptools.version import pkg_resources

import requests
import geopy.exc as geopyexceptions
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from .db import engine
from . import __version__, CONRAD_HOME


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
                state.state["last_check"],
                SELFCHECK_DATE_FMT
            )
            if (current_time - last_check).total_seconds() < 7 * 24 * 60 * 60:
                pypi_version = state.state["pypi_version"]

        # Refresh the version if we need to or just see if we need to warn
        if pypi_version is None:
            pypi_version = get_pypi_version()

            # Save that we've performed a check
            state.save(pypi_version, current_time)

        conrad_version = pkg_resources.parse_version(__version__)
        remote_version = pkg_resources.parse_version(pypi_version)

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


def validate(input_events):
    failures = []

    keys = [
        "name",
        "url",
        "city",
        "state",
        "country",
        "cfp_open",
        "cfp_end_date",
        "start_date",
        "end_date",
        "source",
        "tags",
        "kind",
        "by",
    ]

    # check for duplicates
    ie_names = [ie["name"].replace(" ", "").lower() for ie in input_events]
    if sorted(list(set(ie_names))) != sorted(ie_names):
        failures.append("Duplicate events found")

    # check if keys exist
    for ie in input_events:
        if set(keys).difference(set(ie.keys())):
            failures.append("Required fields not found")
            break

    return failures


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
