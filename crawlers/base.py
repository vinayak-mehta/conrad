# -*- coding: utf-8 -*-

import json
import datetime as dt

from cerberus import Validator


schema = {
    "name": {"type": "string", "minlength": 1, "required": True},
    "url": {"type": "string", "minlength": 1, "required": True},
    "city": {"type": "string", "minlength": 1, "required": True},
    "state": {"type": "string", "required": True, "nullable": True},
    "country": {"type": "string", "minlength": 1, "required": True},
    "cfp_open": {"type": "boolean", "required": True},
    "cfp_end_date": {"is_date": True, "type": "string", "required": True},
    "start_date": {"is_date": True, "type": "string", "required": True},
    "end_date": {"is_date": True, "type": "string", "required": True},
    "source": {"type": "string", "minlength": 1, "required": True},
    "tags": {"type": "list", "minlength": 1, "required": True},
    "kind": {"type": "string", "allowed": ["conference", "meetup"], "required": True},
    "by": {"type": "string", "allowed": ["human", "bot"], "required": True},
}


class EventValidator(Validator):
    def _validate_is_date(self, is_date, field, value):
        """Test if a date is valid.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if is_date:
            valid = True
            try:
                dt.datetime.strptime(value, "%Y-%m-%d")
            except:
                valid = False
            if not valid:
                self._error(field, "must be valid date")


class BaseCrawler(object):
    def __init__(self):
        self.events = []

    def get_events(self):
        pass

    def export(self, filename):
        v = EventValidator(schema)
        for event in self.events:
            v.validate(event)
            if v.errors:
                for key, val in v.errors.items():
                    print("{} - {}: {}".format(event["name"], key, val))

        with open(filename, "w") as f:
            f.write(json.dumps(self.events, indent=4, sort_keys=True))
