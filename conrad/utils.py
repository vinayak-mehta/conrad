# -*- coding: utf-8 -*-

import json
import os
import operator
from jsonschema import Draft4Validator

from .db import engine


def initialize_database():
    from .models import Base

    Base.metadata.create_all(engine)


def reset_database():
    from .models import Base

    Base.metadata.drop_all(engine)
    initialize_database()


def validate(input_events):
    failures = []
    with open(os.path.join(os.path.dirname(__file__), "default_event_schema.json")) as f:
        schema = json.load(f)
    validator = Draft4Validator(schema)

    _errors = sorted(validator.iter_errors(input_events), key=operator.attrgetter('path'))
    error_messages = []
    for err in _errors:
        err_msg = []
        err_msg.append("[%s] -> %s" % ("][".join(repr(index)
                                                 for index in err.absolute_path), err.message))
        for suberror in sorted(err.context, key=operator.attrgetter('schema_path')):
            err_msg.append("  %s" % suberror.message)

        error_messages.append("\n".join(err_msg))

    return error_messages