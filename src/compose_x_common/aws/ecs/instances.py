# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

from typing import Union

from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import chunked_iterable, keyisset


def list_all_instances(
    cluster_id: str,
    instances: list = None,
    next_token: str = None,
    session: Session = None,
    **kwargs,
) -> list:
    """
    List all container instances in a cluster, recursively.
    """
    if instances is None:
        instances: list = []
    session = get_session(session)
    client = session.client("ecs")
    if next_token:
        instances_r = client.list_container_instances(
            cluster=cluster_id, nextToken=next_token, **kwargs
        )
    else:
        instances_r = client.list_container_instances(cluster=cluster_id, **kwargs)
    instances += instances_r["containerInstanceArns"]
    if keyisset("nextToken", instances_r):
        return list_all_instances(
            cluster_id,
            instances,
            next_token=instances_r["nextToken"],
            session=session,
            **kwargs,
        )
    return instances


def describe_all_instances(
    cluster_id: str,
    instances: list = None,
    return_as_mapping: bool = False,
    session: Session = None,
    **kwargs,
) -> Union[list, dict]:
    """
    Describe for all provided container instances in a cluster.
    If no instance given, all instances in the cluster are considered.
    """
    session = get_session(session)
    if instances is None:
        instances: list = list_all_instances(cluster_id, session=session)
    client = session.client("ecs")
    if return_as_mapping:
        instances_defs: dict = {}
    else:
        instances_defs: list = []
    for instances in chunked_iterable(instances, 42):
        instances_r = client.describe_container_instances(
            cluster=cluster_id, containerInstances=instances, **kwargs
        )
        for _instance in instances_r["containerInstances"]:
            if return_as_mapping:
                instances_defs[_instance["containerInstanceArn"]] = _instance
            else:
                instances_defs.append(_instance)
    return instances_defs
