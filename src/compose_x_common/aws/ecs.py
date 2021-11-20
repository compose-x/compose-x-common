#   -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@compose-x.io>

import re
from copy import deepcopy

from boto3.session import Session

from compose_x_common.compose_x_common import chunked_iterable, keyisset

CLUSTER_NAME_FROM_ARN = re.compile(
    r"arn:aws(?:-[a-z-]+)?:ecs:[\S]+:[\d]{12}:cluster/(?P<name>[a-zA-Z0-9-_]+$)"
)


def list_all_ecs_clusters(clusters=None, next_token=None, session=None):
    """

    :param clusters:
    :param next_token:
    :param session:
    :return:
    """
    if clusters is None:
        clusters = []
    if session is None:
        session = Session()
    client = session.client("ecs")
    if next_token:
        clusters_r = client.list_clusters(nextToken=next_token)
    else:
        clusters_r = client.list_clusters()
    if keyisset("nextToken", clusters_r):
        return list_all_ecs_clusters(clusters, clusters_r["nextToken"], session)
    clusters += clusters_r["clusterArns"]
    return clusters


def describe_all_ecs_clusters(
    clusters_to_list: list, session=None, return_as_map=False
):
    """

    :param clusters_to_list:
    :param session:
    :param return_as_map:
    :return:
    """
    clusters = []
    if return_as_map:
        clusters = {}
    if session is None:
        session = Session()
    client = session.client("ecs")
    cluster_chunks = chunked_iterable(clusters_to_list, size=10)
    for clusters_to_describe in cluster_chunks:
        clusters_r = client.describe_clusters(
            clusters=clusters_to_describe,
            include=[
                "ATTACHMENTS",
                "CONFIGURATIONS",
                "SETTINGS",
                "STATISTICS",
                "TAGS",
            ],
        )
        for cluster in clusters_r["clusters"]:
            if return_as_map:
                clusters[cluster["clusterName"]] = cluster
            else:
                clusters.append(cluster)
            clusters.append(cluster)
    return clusters


def list_all_services(
    cluster_name=None, services=None, next_token=None, session=None, **kwargs
):
    """

    :param cluster_name:
    :param services:
    :param next_token:
    :param session:
    :return:
    """
    if services is None:
        services = []
    if session is None:
        session = Session()
    client = session.client("ecs")
    args = deepcopy(kwargs)
    if cluster_name:
        args["cluster"] = cluster_name
    if next_token:
        args["nextToken"] = next_token
    services_r = client.list_services(**args)
    if keyisset("nextToken", services_r):
        return list_all_services(
            cluster_name, services, services_r["nextToken"], session, **args
        )
    services += services_r["serviceArns"]
    return services


def describe_all_services(
    services_list: list, cluster_name=None, session=None, as_map=False, **kwargs
):
    """

    :param list[str] services_list:
    :param str cluster_name:
    :param session:
    :param as_map:
    :return:
    """
    if session is None:
        session = Session()
    client = session.client("ecs")
    chunks = chunked_iterable(services_list, size=10)
    services = []
    if as_map:
        services = {}
    for services_chunk in chunks:
        args = deepcopy(kwargs)
        if cluster_name:
            args["cluster"] = cluster_name
        args["services"] = services_chunk
        services_r = client.describe_services(**args)
        for service in services_r["services"]:
            if as_map:
                services[service["serviceName"]] = service
            else:
                services.append(service)
    return services
