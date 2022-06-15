# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

import re

from boto3.session import Session

from ..compose_x_common import keyisset
from . import get_account_id, get_resource_from_ccapi, get_session

VPC_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:ec2:(?P<region>[a-z\d\-]+-\d):(?P<accounid>[\d]{12}):vpc/(?P<id>vpc-[a-z\d]+)$"
)
SUBNET_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:ec2:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[\d]{12}):subnet/(?P<id>subnet-[a-z\d]+)$"
)


def get_vpc_from_ccapi(vpc_id, session=None, **kwargs):
    """
    Returns VPC properties as per CloudControl API

    :param str vpc_id:
    :param boto3.session.Session session:
    :param dict kwargs:
    :return:
    """
    return get_resource_from_ccapi("AWS::EC2::VPC", vpc_id, session=session, **kwargs)


def get_subnet_from_ccapi(subnet_id, session=None, **kwargs):
    """
    Returns subnet properties as per CloudControl API

    :param str subnet_id:
    :param boto3.session.Session session:
    :param dict kwargs:
    :return:
    """
    return get_resource_from_ccapi(
        "AWS::EC2::Subnet", subnet_id, session=session, **kwargs
    )


def list_all_vpcs(ids_only=False, vpcs=None, next_token=None, session=None, **kwargs):
    """
    List all the VPCs in the account recursively

    :param ids_only:
    :param vpcs:
    :param next_token:
    :param session:
    :param kwargs:
    :return:
    """
    if vpcs is None:
        vpcs = []
    session = get_session(session)
    client = session.client("ec2")
    if next_token:
        vpcs_r = client.describe_vpcs(NextToken=next_token, **kwargs)
    else:
        vpcs_r = client.describe_vpcs(**kwargs)
    vpcs += vpcs_r["Vpcs"]
    if keyisset("NextToken", vpcs_r):
        return list_all_vpcs(ids_only, vpcs, vpcs_r["NextToken"], session, **kwargs)
    if ids_only:
        return [_["VpcId"] for _ in vpcs]
    return vpcs


def get_all_vpcs_from_ccapi(vpc_ids=None, as_map=False, session=None):
    """
    Function to return the VPCs description as per CloudControlApi.
    CCAPI strongly requires that the resource is owned by the same account (shared assets break it).

    :param list[str] vpc_ids:
    :param bool as_map:
    :param boto3.session.Session session:
    :return:
    """
    session = get_session(session)
    vpcs = []
    if as_map:
        vpcs = {}
    if vpc_ids is None:
        vpc_ids = list_all_vpcs(
            ids_only=True,
            session=session,
            Filters=[{"Name": "owner-id", "Values": [get_account_id(session)]}],
        )
    for vpc_id in vpc_ids:
        vpc_def = get_vpc_from_ccapi(vpc_id, session)
        if as_map:
            vpcs[vpc_id] = vpc_def
        else:
            vpcs.append(vpc_def)
    return vpcs


def list_all_subnets(
    ids_only=False, subnets=None, next_token=None, session=None, **kwargs
):
    """
    List all the subnets in the account recursively

    :param ids_only:
    :param subnets:
    :param next_token:
    :param session:
    :param kwargs:
    :return:
    """
    if subnets is None:
        subnets = []
    session = get_session(session)
    client = session.client("ec2")
    if next_token:
        subnet_ids_r = client.describe_subnets(NextToken=next_token, **kwargs)
    else:
        subnet_ids_r = client.describe_subnets(**kwargs)
    subnets += subnet_ids_r["Subnets"]
    if keyisset("NextToken", subnet_ids_r):
        return list_all_subnets(
            ids_only, subnets, subnet_ids_r["NextToken"], session, **kwargs
        )
    if ids_only:
        return [_["SubnetId"] for _ in subnets]
    return subnets


def get_all_subnets_from_ccapi(subnet_ids=None, as_map=False, session=None):
    """
    Function to return the Subnets description as per CloudControlApi.
    CCAPI strongly requires that the resource is owned by the same account (shared assets break it).

    :param list[str] subnet_ids:
    :param bool as_map:
    :param boto3.session.Session session:
    :return:
    """
    session = get_session(session)
    subnets = []
    if as_map:
        subnets = {}
    if subnet_ids is None:
        subnet_ids = list_all_subnets(
            ids_only=True,
            session=session,
            Filters=[{"Name": "owner-id", "Values": [get_account_id(session)]}],
        )
    for subnet_id in subnet_ids:
        subnet_def = get_subnet_from_ccapi(subnet_id, session)
        if as_map:
            subnets[subnet_id] = subnet_def
        else:
            subnets.append(subnet_def)
    return subnets
