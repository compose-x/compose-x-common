#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@compose-x.io>

"""
AWS Useful functions
"""

import re

from boto3.session import Session


def validate_iam_role_arn(arn):
    """
    Function to validate IAM ROLE ARN format
    :param str arn:
    :return: resource match
    :rtype: re.match
    """
    arn_valid = re.compile(r"^arn:aws(?:-[a-z]+)?:iam::[0-9]{12}:role/[\S]+$")
    if not arn_valid.match(arn):
        raise ValueError(
            "The role ARN needs to be a valid ARN of format",
            arn_valid.pattern,
        )
    return arn_valid.match(arn)


def get_assume_role_session(session, arn, session_name=None, region=None):
    """
    Function to override ComposeXSettings session to specific session for Lookup

    :param boto3.session.Session session: The original session fetching the credentials for X-Role
    :param str arn: the IAM Role ARN to assume role with
    :param str session_name: Override name of the session
    :param region: AWS Region for API Calls
    :return: boto3 session from lookup settings
    :rtype: boto3.session.Session
    """
    if not session_name:
        session_name = "stsAssumeRole"
    validate_iam_role_arn(arn)
    if not session:
        session = Session()
    creds = session.client("sts").assume_role(
        RoleArn=arn,
        RoleSessionName=session_name,
        DurationSeconds=900,
    )

    return Session(
        region_name=region,
        aws_access_key_id=creds["Credentials"]["AccessKeyId"],
        aws_session_token=creds["Credentials"]["SessionToken"],
        aws_secret_access_key=creds["Credentials"]["SecretAccessKey"],
    )
