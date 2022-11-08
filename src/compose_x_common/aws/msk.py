# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""AWS MSK Management"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from boto3.session import Session

import re

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset

MSK_CLUSTER_ARN_RE = re.compile(
    r"arn:(?P<partition>[a-z\d\-]+):kafka:(?P<region>[a-z\d\-]+):(?P<accountid>[\d]{12})"
    r":cluster/(?P<id>(?P<name>[\w\-_]+)/(?P<uuid>[a-z0-9\-]+))$"
)

MSK_CONFIGURATION_ARN_RE = re.compile(
    r"arn:(?P<partition>[a-z\d\-]+):kafka:(?P<region>[a-z\d\-]+):(?P<accountid>[\d]{12})"
    r":configuration/(?P<id>(?P<name>[\w\-_]+)/(?P<uuid>[a-z0-9\-]+))$"
)


def list_all_kafka_versions(
    versions: list = None, session: Session = None, **kwargs
) -> list:
    """
    Lists all the versions for MSK
    """
    if versions is None:
        versions: list = []
    session = get_session(session)
    client = session.client("kafka")
    versions_r = client.list_kafka_versions(**kwargs)
    versions += versions_r["KafkaVersions"]
    if keyisset("NextToken", versions_r):
        kwargs.update({"NextToken": versions_r["NextToken"]})
        return list_all_kafka_versions(versions, session, **kwargs)
    return versions


def list_all_kafka_configurations(
    configurations: list = None, session: Session = None, **kwargs
) -> list:
    """
    Lists all the configurations for MSK
    """
    if configurations is None:
        configurations: list = []
    session = get_session(session)
    client = session.client("kafka")
    configurations_r = client.list_configurations(**kwargs)
    configurations += configurations_r["Configurations"]
    if keyisset("NextToken", configurations_r):
        kwargs.update({"NextToken": configurations_r["NextToken"]})
        return list_all_kafka_configurations(configurations, session, **kwargs)
    return configurations


def list_all_kafka_clusters(
    clusters: list = None, session: Session = None, **kwargs
) -> list:
    """
    Lists all the clusters for MSK
    """
    if clusters is None:
        clusters: list = []
    session = get_session(session)
    client = session.client("kafka")
    clusters_r = client.list_clusters(**kwargs)
    clusters += clusters_r["ClusterInfoList"]
    if keyisset("NextToken", clusters_r):
        kwargs.update({"NextToken": clusters_r["NextToken"]})
        return list_all_kafka_clusters(clusters, session, **kwargs)
    return clusters


def list_all_kafka_clusters_v2(
    clusters: list = None, session: Session = None, **kwargs
) -> list:
    """
    Lists all the clusters for MSK
    """
    if clusters is None:
        clusters: list = []
    session = get_session(session)
    client = session.client("kafka")
    clusters_r = client.list_clusters_v2(**kwargs)
    clusters += clusters_r["ClusterInfoList"]
    if keyisset("NextToken", clusters_r):
        kwargs.update({"NextToken": clusters_r["NextToken"]})
        return list_all_kafka_clusters(clusters, session, **kwargs)
    return clusters


if __name__ == "__main__":
    print(list_all_kafka_clusters())
    print(list_all_kafka_clusters_v2())
