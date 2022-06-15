# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>


import re
import warnings

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset

KMS_KEY_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:kms:(?P<region>[a-z\d\-]+-\d):(?P<accountid>\d{12}):key/"
    r"(?P<id>[a-zA-Z\d]{8}(?:-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12})$"
)
KMS_ALIAS_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:kms:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[0-9]{12}):(?P<id>alias/[\S]+)$"
)


def list_all_keys(keys=None, next_token=None, session=None):
    """
    Function to list all the KMS keys the session allows

    :param list keys:
    :param str next_token:
    :param boto3.session.Session session:
    :return:
    """
    session = get_session(session)
    if keys is None:
        keys = []
    client = session.client("kms")
    if not next_token:
        keys_r = client.list_keys()
    else:
        keys_r = client.list_keys(Marker=next_token)
    if keyisset("Keys", keys_r):
        keys += keys_r["Keys"]
    else:
        return keys
    if keyisset("NextMarker", keys_r):
        keys += list_all_keys(keys, keys_r["NextMarker"], session)
    return keys


def list_all_aliases(aliases=None, next_token=None, session=None):
    """
    Function to list all the KMS keys the session allows

    :param list aliases:
    :param str next_token:
    :param boto3.session.Session session:
    :return:
    """
    session = get_session(session)
    client = session.client("kms")
    if aliases is None:
        aliases = []
    if not next_token:
        aliases_r = client.list_aliases()
    else:
        aliases_r = client.list_aliases(Marker=next_token)
    if keyisset("Aliases", aliases_r):
        aliases += aliases_r["Aliases"]
    else:
        return aliases
    if keyisset("NextMarker", aliases_r):
        aliases += list_all_aliases(aliases, aliases_r["NextMarker"], session)
    return aliases


def get_key_from_alias(alias, keys=None, alias_failback=False, session=None):
    """

    :param str alias: The alias or part of it that we are looking for.
    :param list keys:
    :param bool alias_failback:
    :param boto3.session.Session session:
    :return:
    """
    if not alias.startswith("alias/"):
        warnings.warn("The alias must start with alias/. Adding alias/")
        alias = f"alias/{alias}"
    session = get_session(session)
    aliases = list_all_aliases(session=session)
    if not keys:
        keys = list_all_keys(session=session)
    for _alias in aliases:
        if alias.startswith("alias/") and _alias["AliasName"] == alias:
            for key in keys:
                if (
                    keyisset("TargetKeyId", _alias)
                    and key["KeyId"] == _alias["TargetKeyId"]
                ):
                    return key
            if alias_failback:
                return _alias
    return None
