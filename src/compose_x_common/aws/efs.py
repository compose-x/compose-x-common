# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2024 John Mille <john@compose-x.io>

from __future__ import annotations

import re
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset

EFS_ARN_RE = re.compile(
    r"^arn:(?P<partition>aws(?:-[a-z]+)?):elasticfilesystem:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[0-9]{12}):file-system/(?P<id>[\S]+)$"
)


def list_efs_mount_targets(
    mount_points: list = None,
    next_token: str = None,
    session: Session = None,
    client=None,
    **kwargs,
) -> list:
    """
    Wrapper function for `describe_mount_targets`
    Returns list of mount targets based on the Parameter used to filter the request in the Kwargs, one of
        FileSystemId='string'
        MountTargetId='string'
        AccessPointId='string
    """
    session = get_session(session)
    client = client or session.client("efs")
    if mount_points is None:
        mount_points: list = []
    if next_token:
        kwargs.update({"NextMarker": next_token})
    response = client.describe_mount_targets(**kwargs)
    if not keyisset("MountTargets", response):
        return mount_points
    mount_points += response["MountTargets"]
    if keyisset("NextMarker", response):
        return list_efs_mount_targets(
            mount_points, response["NextMarker"], session, client
        )
    return mount_points
