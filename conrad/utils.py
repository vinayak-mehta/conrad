# -*- coding: utf-8 -*-

from .db import engine

import geopy.exc as geopyexceptions
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
# open street maps nominatim geocoder
geolocator = Nominatim(user_agent='conrad')
# Delay between geocoding calls to not run out of calls
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)


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


"""Function is deliberately made recursive
    to avoid timeout error
"""
def standard_address(place):
    """Return the standard address
    as dict given the name of a place

    place (str): name of the place
    returs (dict): standard address
    """
    try:
        location = geolocator.geocode(place)
        if location:
            address = geolocator.reverse(
                "{lat}, {lon}".format(lat=location.latitude, lon=location.longitude)
            ).raw["address"]
            address['latitude'] = location.latitude
            address['longitude'] = location.longitude
        else:
            # unable to geocode :(
            address = {}
        return address
    except geopyexceptions.GeocoderTimedOut:
        # Timeout try again
        standard_address(place)
