# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

from typing import Union

from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import chunked_iterable, keyisset


def list_all_tasks(
    cluster_id: str,
    tasks: list = None,
    next_token: str = None,
    session: Session = None,
    **kwargs,
) -> list:
    """
    List all tasks in a cluster, recursively.
    """
    if tasks is None:
        tasks: list = []
    session = get_session(session)
    client = session.client("ecs")
    if next_token:
        tasks_r = client.list_tasks(cluster=cluster_id, nextToken=next_token, **kwargs)
    else:
        tasks_r = client.list_tasks(cluster=cluster_id, **kwargs)
    tasks += tasks_r["taskArns"]
    if keyisset("nextToken", tasks_r):
        return list_all_tasks(
            cluster_id,
            tasks,
            next_token=tasks_r["nextToken"],
            session=session,
            **kwargs,
        )
    return tasks


def describe_all_tasks(
    cluster_id: str,
    tasks: list = None,
    return_as_mapping: bool = False,
    session: Session = None,
    **kwargs,
) -> Union[list, dict]:
    """
    Describe for all provided tasks in a cluster. If no tasks are given, all tasks in the cluster are considered.
    """
    session = get_session(session)
    if tasks is None:
        tasks: list = list_all_tasks(cluster_id, session=session)
    client = session.client("ecs")
    if return_as_mapping:
        tasks_defs: dict = {}
    else:
        tasks_defs: list = []
    for tasks in chunked_iterable(tasks, 42):
        tasks_r = client.describe_tasks(cluster=cluster_id, tasks=tasks, **kwargs)
        for _task in tasks_r["tasks"]:
            if return_as_mapping:
                tasks_defs[_task["taskArn"]] = _task
            else:
                tasks_defs.append(_task)
    return tasks_defs
