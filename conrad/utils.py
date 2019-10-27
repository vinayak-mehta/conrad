# -*- coding: utf-8 -*-

import json

from .db import engine


def initialize_database():
    from .models import Base

    Base.metadata.create_all(engine)


def reset_database():
    from .models import Base

    Base.metadata.drop_all(engine)
    initialize_database()


def validate_import():
    # check for duplicates
    # check if keys exist
    pass
