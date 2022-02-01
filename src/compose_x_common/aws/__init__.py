#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@compose-x.io>

"""
AWS Useful functions
"""
import json
import re
from copy import deepcopy

from boto3.session import Session

from ..compose_x_common import set_else_none


def get_session(session=None):
    """
    Simple function to assign a new session when none given

    :param session:
    :return: session
    :rtype: boto3.session.Session
    """
    if session is None:
        return Session()
    return session


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


def get_assume_role_session(session, arn, session_name=None, region=None, **kwargs):
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


def get_resource_from_ccapi(type_name: str, identifier, session=None, **kwargs):
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


def get_region_azs(session=None):
    """Function to return the AZ from a given region. Uses default region for this

    :param boto3.session.Session session: Boto3 session

    :return: list of AZs in the given region
    :rtype: list
    """
    session = get_session(session)
    return session.client("ec2").describe_availability_zones()["AvailabilityZones"]


def get_account_id(session=None):
    """
    Function to get the current session account ID

    :param boto3.session.Session session: Boto3 Session to make the API call.

    :return: account ID
    :rtype: str
    """
    session = get_session(session)
    return session.client("sts").get_caller_identity()["Account"]
