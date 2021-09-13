# -*- coding: utf-8 -*-
from crawlers import base


def test_validate_is_date():
    """ Testing that validator does not raise exception given a correctly formatted date string """
    date_string = "2020-08-15"
    base.EventValidator()._validate_is_date(True, "Date", date_string)
