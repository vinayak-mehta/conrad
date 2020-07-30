# -*- coding: utf-8 -*-

import os
import json
import datetime as dt

from cerberus import Validator

from .schema import _v1, _v2, LATEST


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

    def export(self, filename, version="2"):
        _schema = eval(f"_v{LATEST}")

        if version == LATEST:
            v = EventValidator(_schema)
            for event in self.events:
                v.validate(event)
                if v.errors:
                    for key, val in v.errors.items():
                        print(f"{event['name']} - {key}: {val}")

        events = []
        for event in self.events:
            _event = dict({k: v for k, v in event.items() if k in _schema.keys()})
            events.append(_event)

        export_dir = os.path.dirname(filename)
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        with open(filename, "w") as f:
            f.write(json.dumps(events, indent=4, sort_keys=True))
