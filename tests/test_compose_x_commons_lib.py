#!/usr/bin/env python

"""Tests for `compose_x_common` package."""

from datetime import datetime as dt
from os import path

import pytest
from dateutil.relativedelta import relativedelta

from compose_x_common.compose_x_common import (
    attributes_to_mapping,
    get_duration,
    get_future_time_delta,
    get_past_time_delta,
    keyisset,
    keypresent,
)

HERE = path.abspath(path.dirname(__file__))


@pytest.fixture()
def test_d():
    return {"true": True, "false": False, "empty_list": [], "listing": [1, 2, 3]}


def test_empty_dict(test_d):
    assert not keyisset("no", test_d)
    assert not keypresent("no", test_d)


def test_present_key(test_d):
    assert not keyisset("false", test_d)
    assert keypresent("empty_list", test_d)
    assert keypresent("false", test_d)


def test_key_is_set(test_d):
    assert keyisset("listing", test_d)
    assert keypresent("empty_list", test_d)


def test_get_duration():
    assert get_duration("10m") == relativedelta(minutes=10)
    assert get_duration("1y") == relativedelta(years=1)
    assert get_duration("4d") == relativedelta(days=4)
    assert get_duration("1w") == relativedelta(weeks=1)
    assert get_duration("1y2w4d") == relativedelta(years=1, weeks=2, days=4)


def test_time_delta():
    now = dt.utcnow()
    delta = get_duration("10m")
    delta_test = relativedelta(minutes=10)
    assert get_future_time_delta(now, delta) == get_future_time_delta(now, delta_test)
    assert get_past_time_delta(now, delta) == get_past_time_delta(now, delta_test)


def test_attribute_to_mapping():
    input_mapping = {
        "Name": "Name",
        "Age": "details::age",
        "Married": "details::status::married",
    }

    john = {"Name": "John", "details": {"age": 42, "status": {"married": False}}}
    john_test = attributes_to_mapping(john, input_mapping)
    assert john_test == {"Name": "John", "Age": 42, "Married": False}


def test_attribute_to_mapping_missing_attr():
    input_mapping = {
        "Name": "Name",
        "Age": "details.age",
        "Married": "details.status.married",
    }

    john = {
        "Name": "John",
        "details": {
            "age": 42,
        },
    }
    john_test = attributes_to_mapping(john, input_mapping, ".")
    assert john_test == {"Name": "John", "Age": 42}
