#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@compose-x.io>

"""
Main module.
"""


import itertools
import re
import warnings
from os import environ

from dateutil.relativedelta import relativedelta

DURATIONS_RE = re.compile(
    r"(((?P<y>[0-9]+)y)?((?P<w>[0-9]+)w)?((?P<d>[0-9]+)d)?((?P<h>[0-9]+)h)"
    r"?((?P<m>[0-9]+)m)?((?P<s>[0-9]+)s)?((?P<ms>[0-9]+)ms)?|0)"
)


def keyisset(key, y):
    """
    Macro to figure if the the dictionary contains a key and that the key is not empty

    :param key: The key to check presence in the dictionary
    :type key: str
    :param y: The dictionary to check for
    :type y: dict

    :returns: True/False
    :rtype: bool
    """
    if isinstance(y, dict) and key in y.keys() and y[key]:
        return True
    return False


def keypresent(key, y):
    """
    Macro to figure if the the dictionary contains a key and that the key is not empty

    :param key: The key to check presence in the dictionary
    :type key: str
    :param y: The dictionary to check for
    :type y: dict

    :returns: True/False
    :rtype: bool
    """
    if isinstance(y, dict) and key in y.keys():
        return True
    return False


def get_duration(time_from, duration_exp, env_key=None):
    """
    Function to define the time delta

    :param datetime.datetime time_from:
    :param str duration_exp:
    :param str env_key:
    :return: datetime of the delta between from_time until expressed duration
    """
    if isinstance(env_key, str):
        duration_exp = environ.get(env_key, duration_exp)
    else:
        duration_exp = environ.get("ECR_IMAGES_DURATION_DELTA", duration_exp)
    if not DURATIONS_RE.match(duration_exp):
        warnings.warn(
            f"The provided duration, {duration_exp}, does not match expected regexp "
            f"{DURATIONS_RE.pattern}. Using default of 7days"
        )
    parts = DURATIONS_RE.match(duration_exp)
    milliseconds = int(parts.group("ms")) if parts.group("ms") else 0
    seconds = int(parts.group("s")) if parts.group("s") else 0
    minutes = int(parts.group("m")) if parts.group("m") else 0
    hours = int(parts.group("h")) if parts.group("h") else 0
    days = int(parts.group("d")) if parts.group("d") else 0
    weeks = int(parts.group("w")) if parts.group("w") else 0
    years = int(parts.group("y")) if parts.group("y") else 0
    up_to = time_from + relativedelta(
        years=years,
        minutes=minutes,
        weeks=weeks,
        days=days,
        hours=hours,
        seconds=seconds,
        microseconds=(milliseconds * 1000),
    )
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
