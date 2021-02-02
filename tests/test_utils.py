# -*- coding: utf-8 -*-
from conrad import utils


def test_get_address():
    """ Testing that utils.get_address can successfully resolve supported and unsupported addresses """
    nyc_address = {
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
    # Unsupported location
    place = 'doesnotexist'
    address = utils.get_address(place)
    assert address is None
    # Supported location
    place = 'New York'
    address = utils.get_address(place)
    assert address == nyc_address


def test_validate_events():
    """ Testing that validate events can identify duplicate events and events with incorrect schemas """
    # Events with duplicate names
    expected_failure_with_duplicates = "Duplicate events found"
    events_with_duplicates = [{"name": "Event1"}, {"name": "  Event1  "}, {"name": "Event2"}]
    actual_failures = utils.validate_events(events_with_duplicates)
    assert expected_failure_with_duplicates in actual_failures
    events_with_duplicates = [{"name": "EvEnT1"}, {"name": "  event1  "}]
    actual_failures = utils.validate_events(events_with_duplicates)
    assert expected_failure_with_duplicates in actual_failures

    # Events without any duplicate names
    events_without_duplicates = [{"name": "Event1"}, {"name": "Event2"}]
    actual_failures = utils.validate_events(events_without_duplicates)
    assert expected_failure_with_duplicates not in actual_failures

    # Events with missing fields required by the schema
    expected_failures_incorrect_schema = "Required fields not found"
    events_with_bad_schema = [{"name": "Name1"}, {"name": "Name2"}]
    actual_failures = utils.validate_events(events_with_bad_schema)
    assert expected_failures_incorrect_schema in actual_failures

    # TODO add good schema check and latest version resolve check


def test_apply_schema():
    """ Testing that utils.apply_schema can successfully apply the given schema to a collection of
    events """
    # Events contain fields that are not in the schema
    events = [
        {"name": "Event1", "city": "New York", "state": "NY", "type": "conf"},
        {"name": "Event2", "city": "Seattle", "state": "WA", "type": "conf", "speaker": "John Doe"}
    ]
    # A filtered down collection of events with only fields in schema is expected
    expected_events = [
        {"name": "Event1", "city": "New York", "state": "NY"},
        {"name": "Event2", "city": "Seattle", "state": "WA"}
    ]
    result = utils.apply_schema(events)
    assert result == expected_events

    # Events contain only fields that are in the schema
    events = [
        {"name": "Name1", "city": "Austin", "state": "TX"},
        {"name": "Name2", "city": "Portland", "state": "OR"}
    ]
    result = utils.apply_schema(events)
    # No fields to filter out so the same unmodified collection of events is expected
    assert events == result

    # Events contain only fields that are not in the schema
    events = [
        {"event_id": "A124FDVWi2", "type": "conf"},
        {"event_id": "B243SDFS23", "type": "conf", "speaker": "Jane Doe"}
    ]
    result = utils.apply_schema(events)
    # A list of empty event objects is expected
    assert [{}, {}] == result
