#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@compose-x.io>

"""
Main module.
"""


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
