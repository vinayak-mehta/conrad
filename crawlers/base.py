# -*- coding: utf-8 -*-

import os
import json
import datetime as dt

from cerberus import Validator

from conrad.schema import latest


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
        v = EventValidator(latest)
        for event in self.events:
            v.validate(event)
            if v.errors:
                for key, val in v.errors.items():
                    print(f"{event['name']} - {key}: {val}")

        with open(filename, "w") as f:
            f.write(json.dumps(events, indent=4, sort_keys=True))
