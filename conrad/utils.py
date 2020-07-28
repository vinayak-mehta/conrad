# -*- coding: utf-8 -*-

from .db import engine

import geopy.exc as geopyexceptions
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


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
