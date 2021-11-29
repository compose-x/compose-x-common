#    -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>


from os import path

import placebo
from boto3.session import Session

from compose_x_common.aws.resourcegroupstaggingapi import (
    find_aws_resource_arn_from_tags_api,
)
from compose_x_common.aws.vpc import (
    VPC_ARN_RE,
    get_all_subnets_from_ccapi,
    get_all_vpcs_from_ccapi,
    list_all_subnets,
    list_all_vpcs,
)

HERE = path.abspath(path.dirname(__file__))


def test_get_vpcs():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/vpc/")
    # pill.record()
    pill.playback()
    list_all_vpcs()
    vpc_def = get_all_vpcs_from_ccapi(session=test_session)
    print(vpc_def)


def test_get_subnets():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/vpc/")
    # pill.record()
    pill.playback()
    list_all_subnets()
    vpc_def = get_all_subnets_from_ccapi(session=test_session)
    print(vpc_def)


def test_find_from_tags():

    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/vpc/")
    # pill.record()
    pill.playback()
    tags = [{"Key": "Name", "Values": ("test123",)}]
    vpc_arns = find_aws_resource_arn_from_tags_api(
        "ec2:vpc", tags, session=test_session
    )
    print(vpc_arns)
    vpc_ids = [VPC_ARN_RE.match(arn).group("id") for arn in vpc_arns]
    vpc_def = get_all_vpcs_from_ccapi(vpc_ids, session=test_session)
    print(vpc_def)
