# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

import re

from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset

SERVICE_ARN_RE = re.compile(
    r"arn:(?P<partition>aws(?:[^:]+)?):ecs:(?P<region>[^:]+):"
    r"(?P<account_id>\d{12}):service/(?P<cluster>[^/][\w\-_]+)/(?P<id>[^/]+)"
)


def get_ecs_services_from_tags(
    tags: list,
    services_list: list = None,
    next_token: str = None,
    session: Session = None,
    arns_only: bool = False,
) -> list:
    """
    Retrieves the services based on the tags provided.
    Returns the services ARNs

    :return:
    """
    if services_list is None:
        services_list: list = []
    session = get_session(session)
    client = session.client("resourcegroupstaggingapi")
    if next_token:
        services_r = client.get_resources(
            TagFilters=tags,
            ResourceTypeFilters=["ecs:service"],
            PaginationToken=next_token,
        )
        services_list += services_r["ResourceTagMappingList"]
    else:
        services_r = client.get_resources(
            TagFilters=tags, ResourceTypeFilters=["ecs:service"]
        )
        services_list += services_r["ResourceTagMappingList"]
    if keyisset("PaginationToken", services_r):
        return get_ecs_services_from_tags(
            tags, services_list, services_r["PaginationToken"], session
        )
    if arns_only:
        return [item["ResourceARN"] for item in services_list]
    return services_list
