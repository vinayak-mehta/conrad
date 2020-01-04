"""-*- coding: utf-8 -*-."""

from conrad.utils import standard_address

NYC_ADDRESS = {
    "townhall": "New York City Hall",
    "house_number": "260",
    "road": "Broadway",
    "suburb": "Manhattan",
    "city": "New York",
    "county": "New York County",
    "state": "New York",
    "postcode": "10000",
    "country": "United States of America",
    "country_code": "us",
    "latitude": 40.7127281,
    "longitude": -74.0060152,
}


def test_standard_address():
    """Test standard address geocoding."""
    bad_place = "doesnotexist"
    empty = standard_address(bad_place)
    good_place = "New York"
    nyc = standard_address(good_place)
    assert (empty, nyc) == ({}, nyc)
