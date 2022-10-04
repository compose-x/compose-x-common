# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

import re
from typing import Union

"""
AWS Useful functions
"""
import json
from copy import deepcopy

from boto3.session import Session

from compose_x_common.aws.iam import IAM_ROLE_ARN_RE
from compose_x_common.compose_x_common import set_else_none


def get_session(session: Session = None) -> Session:
    """
    Simple function to assign a new session when none given

    :param session:
    :return: session
    :rtype: boto3.session.Session
    """
    if session is None:
        return Session()
    return session


def validate_iam_role_arn(arn: str, as_str: bool = False) -> Union[str, re.Match]:
    """
    Function to validate IAM ROLE ARN format

    :param str arn:
    :param bool as_str: returns the role ARN as a string
    :return: resource match
    :rtype: re.match
    """
    match = IAM_ROLE_ARN_RE.match(arn)
    if not match:
        raise ValueError(
            "The role ARN needs to be a valid ARN of format",
            IAM_ROLE_ARN_RE.pattern,
        )
    if as_str:
        return arn
    return match


def get_assume_role_session(
    session: Session, arn: str, session_name: str = None, region: str = None, **kwargs
) -> Session:
    """
    Function to override ComposeXSettings session to specific session for Lookup

    :param boto3.session.Session session: The original session fetching the credentials for X-Role
    :param str arn: the IAM Role ARN to assume role with
    :param str session_name: Override name of the session
    :param region: AWS Region for API Calls
    :return: boto3 session from lookup settings
    :rtype: boto3.session.Session
    """
    args = deepcopy(kwargs)
    if not session_name or "RoleSessionName" not in kwargs.keys():
        args["RoleSessionName"] = "stsAssumeRole"
    args["RoleArn"] = arn
    args["DurationSeconds"] = set_else_none("DurationSeconds", kwargs, alt_value=900)
    validate_iam_role_arn(arn)
    creds = session.client("sts").assume_role(**args)

    return Session(
        region_name=region,
        aws_access_key_id=creds["Credentials"]["AccessKeyId"],
        aws_session_token=creds["Credentials"]["SessionToken"],
        aws_secret_access_key=creds["Credentials"]["SecretAccessKey"],
    )


def get_resource_from_ccapi(
    type_name: str, identifier: Union[str, dict], session: Session = None, **kwargs
) -> dict:
    """
    Wrapper around cloudcontrol.get_resource

    :param str type_name:
    :param str|dict identifier:
    :param boto3.session.Session session:
    :param dict kwargs:
    :return:
    """
    session = get_session(session)
    client = session.client("cloudcontrol")
    resource_r = client.get_resource(
        TypeName=type_name, Identifier=identifier, **kwargs
    )
    resource_properties = json.loads(resource_r["ResourceDescription"]["Properties"])
    return resource_properties


def get_region_azs(session: Session = None) -> list:
    """Function to return the AZ from a given region. Uses default region for this

    :param boto3.session.Session session: Boto3 session

    :return: list of AZs in the given region
    :rtype: list
    """
    session = get_session(session)
    return session.client("ec2").describe_availability_zones()["AvailabilityZones"]


def get_account_id(session: Session = None) -> str:
    """
    Function to get the current session account ID

    :param boto3.session.Session session: Boto3 Session to make the API call.

    :return: account ID
    :rtype: str
    """
    session = get_session(session)
    return session.client("sts").get_caller_identity()["Account"]
