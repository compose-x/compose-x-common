# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""
Main module.
"""

from __future__ import annotations

import itertools
import re
from typing import Any, Union

from dateutil.relativedelta import relativedelta
from flatdict import FlatDict, FlatterDict

DURATIONS_RE = re.compile(
    r"(((?P<y>[0-9]+)y)?((?P<w>[0-9]+)w)?((?P<d>[0-9]+)d)?((?P<h>[0-9]+)h)"
    r"?((?P<m>[0-9]+)m)?((?P<s>[0-9]+)s)?((?P<ms>[0-9]+)ms)?|0)"
)


def keyisset(key, y: Union[dict, FlatDict, FlatterDict]) -> bool:
    """
    Macro to figure if the dictionary contains a key and that the key is not empty

    :param key: The key to check presence in the dictionary
    :type key: str
    :param y: The dictionary to check for
    :type y: dict

    :returns: True/False
    :rtype: bool
    """
    if isinstance(y, (FlatterDict, FlatDict, dict)) and key in y.keys() and y[key]:
        return True
    return False


def keypresent(key, y: Union[dict, FlatDict, FlatterDict]) -> bool:
    """
    Macro to figure if the dictionary contains a key and that the key is not empty

    :param key: The key to check presence in the dictionary
    :type key: str
    :param y: The dictionary to check for
    :type y: dict

    :returns: True/False
    :rtype: bool
    """
    if isinstance(y, (FlatterDict, FlatDict, dict)) and key in y.keys():
        return True
    return False


def set_else_none(
    key: Any,
    props: Union[dict, FlatDict, FlatterDict],
    alt_value: Any = None,
    eval_bool: bool = False,
) -> Any:
    """
    Function to serialize if not keyisset () set other value

    :param str key:
    :param dict props:
    :param alt_value:
    :param bool eval_bool: Allows to gets booleans properties
    :return:
    """
    if not eval_bool:
        return alt_value if not keyisset(key, props) else props[key]
    elif eval_bool:
        return alt_value if not keypresent(key, props) else props[key]


def get_duration(duration_exp: str) -> relativedelta:
    """
    Function to define the time delta
    """
    parts = DURATIONS_RE.match(duration_exp)
    milliseconds = int(parts.group("ms")) if parts.group("ms") else 0
    seconds = int(parts.group("s")) if parts.group("s") else 0
    minutes = int(parts.group("m")) if parts.group("m") else 0
    hours = int(parts.group("h")) if parts.group("h") else 0
    days = int(parts.group("d")) if parts.group("d") else 0
    weeks = int(parts.group("w")) if parts.group("w") else 0
    years = int(parts.group("y")) if parts.group("y") else 0
    delta = relativedelta(
        years=years,
        minutes=minutes,
        weeks=weeks,
        days=days,
        hours=hours,
        seconds=seconds,
        microseconds=(milliseconds * 1000),
    )
    return delta


def get_future_time_delta(time_from, delta):
    up_to = time_from + delta
    return up_to


def get_past_time_delta(time_from, delta):
    up_to = time_from - delta
    return up_to


def chunked_iterable(iterable, size):
    """
    Function to make chunks from iterable type
    `Source <https://alexwlchan.net/2018/12/iterating-in-fixed-size-chunks/>`__

    :param iterable:
    :param size:
    :return:
    """
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


def attributes_to_mapping(input_obj, mapping, separator=None):
    """
    Simple function returning all the
    :param dict input_obj:
    :param dict mapping:
    :param separator: The separator for nested properties of mapping. Defaults to '::'
    :return:
    """
    if separator is None:
        separator = "::"
    flat = FlatterDict(input_obj)
    flat.set_delimiter(separator)
    result = {}
    for key, attr in mapping.items():
        if keypresent(attr, flat) and not isinstance(flat[attr], list):
            result[key] = flat[attr]
    return result
