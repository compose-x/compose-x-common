# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>


from __future__ import annotations

import re
from typing import Union

from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset

USER_POOL_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:cognito-idp:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[\d]{12}):userpool/(?P<id>[\S]+)$"
)


def list_all_user_pools(
    user_pools: list = None, next_token: str = None, session: Session = None, **kwargs
) -> list:
    session = get_session(session)
    if user_pools is None:
        user_pools = []
    if not keyisset("MaxResults", kwargs):
        kwargs.update({"MaxResults": 20})
    if not next_token:
        user_pools_r = session.client("cognito-idp").list_user_pools(**kwargs)
    else:
        user_pools_r = session.client("cognito-idp").list_user_pools(
            NextToken=next_token, **kwargs
        )
    user_pools += user_pools_r["UserPools"]
    if keyisset("NextToken", user_pools_r):
        return list_all_user_pools(
            user_pools, user_pools_r["NextToken"], session, **kwargs
        )
    return user_pools


def describe_all_user_pools(
    user_pools_ids: list = None, session: Session = None, as_mapping: bool = False
) -> Union[list, dict]:
    session = get_session(session)
    if user_pools_ids is None:
        user_pools_ids = [_pool["Id"] for _pool in list_all_user_pools(session=session)]
    client = session.client("cognito-idp")
    if as_mapping:
        user_pools_details: dict = {}
        for pool_id in user_pools_ids:
            user_pools_details[pool_id] = client.describe_user_pool(UserPoolId=pool_id)[
                "UserPool"
            ]
    else:
        user_pools_details: list = []
        for pool_id in user_pools_ids:
            user_pools_details.append(
                client.describe_user_pool(UserPoolId=pool_id)["UserPool"]
            )
    return user_pools_details
