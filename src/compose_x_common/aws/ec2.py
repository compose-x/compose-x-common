# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2024 John Mille <john@compose-x.io>

"""EC2 toolbox"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from boto3.session import Session

from botocore.exceptions import ClientError

from compose_x_common.aws import get_session


def get_ec2_subnet_from_vpc_and_ip_cidr(
    ip_cidr: str, vpc_id: str = None, session: Session = None
) -> dict:
    """Function to get the Subnet details from subnet CIDR and filter with VPC ID if provided"""
    session = get_session(session)
    client = session.client("ec2")
    filters = [
        {"Name": "cidr-block", "Values": [ip_cidr]},
    ]
    if vpc_id:
        filters.append(
            {"Name": "vpc-id", "Values": [vpc_id]},
        )
    try:
        subnets_r = client.describe_subnets(Filters=filters)
        return subnets_r["Subnets"][0]
    except ClientError as error:
        print("Failed to retrieve Subnet from VPC ID and CIDR", error)
        return {}
    except Exception as error:
        print("An exception occurred", error)
        raise
