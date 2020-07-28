# -*- coding: utf-8 -*-

from conrad.utils import get_address


NYC_ADDRESS = {
    "amenity": "New York City Hall",
    "house_number": "260",
    "road": "Broadway",
    "neighbourhood": "Civic Center",
    "suburb": "Manhattan",
    "city": "Manhattan Community Board 1",
    "county": "New York County",
    "state": "New York",
    "postcode": "10000",
    "country": "United States of America",
    "country_code": "us",
    "latitude": 40.7127281,
    "longitude": -74.0060152,
}


def test_bad_place():
    place = "doesnotexist"
    address = get_address(place)
    assert address is None


def test_good_place():
    place = "New York"
    address = get_address(place)
    assert address == NYC_ADDRESS
