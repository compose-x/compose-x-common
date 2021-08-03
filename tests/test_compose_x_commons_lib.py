#!/usr/bin/env python

"""Tests for `compose_x_common` package."""

import pytest

from compose_x_common.compose_x_common import keyisset, keypresent


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
