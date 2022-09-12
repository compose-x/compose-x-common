# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>


import re

SECRET_ARN_RE = re.compile(
    r"^arn:aws(?:[\w-]+)?:secretsmanager:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[0-9]{12}):"
    r"secret:(?P<id>[\S]+-[A-Za-z\d]{6})$"
)


def get_secret_name_from_arn(secret_arn: str):
    """
    Function to get the secret name from the secret ARN. The ARN contains a `-` with 6 random chars.
    The secret name needs these removed, so we remove the last 7 chars from the secret ARN

    :param str secret_arn:
    :return: The secret name
    :rtype: str
    :raises: ValueError if invalid ARN
    """
    if not SECRET_ARN_RE.match(secret_arn):
        raise ValueError(
            "Secret ARN is not valid. Must match regex", SECRET_ARN_RE.pattern
        )
    secret_id = SECRET_ARN_RE.match(secret_arn).group("id")
    return secret_id[:-7]
