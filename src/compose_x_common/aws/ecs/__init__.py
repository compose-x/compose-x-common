# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

import json
import re
from copy import deepcopy

import boto3
from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import chunked_iterable, keyisset

CLUSTER_NAME_FROM_ARN = re.compile(
    r"arn:aws(?:-[a-z-]+)?:ecs:(?P<region>[a-z\d\-]+-\d):(?P<accountid>\d{12}):"
    r"cluster/(?P<name>[\w\-_]+)$"
)

CLUSTER_ID_ARN_RE = re.compile(
    r"arn:aws(?:-[a-z-]+)?:ecs:(?P<region>[a-z\d\-]+-\d):(?P<accountid>\d{12}):"
    r"cluster/(?P<id>[\w\-_]+)$"
)


def list_all_ecs_clusters(clusters=None, next_token=None, session=None, **kwargs):
    """

    :param clusters:
    :param next_token:
    :param session:
    :param kwargs: Additional API parameters for ecs.list_clusters()
    :return:
    """
    if clusters is None:
        clusters = []
    session = get_session(session)
    client = session.client("ecs")
    if next_token:
        clusters_r = client.list_clusters(nextToken=next_token, **kwargs)
    else:
        clusters_r = client.list_clusters(**kwargs)
    clusters += clusters_r["clusterArns"]
    if keyisset("nextToken", clusters_r):
        return list_all_ecs_clusters(
            clusters, clusters_r["nextToken"], session, **kwargs
        )
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
    session = get_session(session)
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
                clusters[cluster["clusterArn"]] = cluster
            else:
                clusters.append(cluster)
    return clusters


def describe_all_ecs_clusters_from_ccapi(
    clusters_to_list: list, return_as_map=False, use_cluster_name=False, session=None
):
    """
    Function to retrieve all clusters config based on AWS CloudControl API

    :param list[str] clusters_to_list: list of ECS cluster ARN to describe
    :param bool return_as_map: Whether to return the clusters into a dict instead of a list
    :param bool use_cluster_name: Use the cluster name (from ARN) instead of the ARN
    :param boto3.session.Session session: override boto3 session
    :return:
    """
    clusters = []
    if return_as_map:
        clusters = {}
    session = get_session(session)
    client = session.client("cloudcontrol")
    for cluster_arn in clusters_to_list:
        cluster_r = client.get_resource(
            TypeName="AWS::ECS::Cluster", Identifier=cluster_arn
        )
        cluster_properties = json.loads(cluster_r["ResourceDescription"]["Properties"])
        if return_as_map:
            if use_cluster_name:
                clusters[
                    CLUSTER_NAME_FROM_ARN.match(cluster_arn).group("name")
                ] = cluster_properties
            else:
                clusters[cluster_arn] = cluster_properties
        else:
            clusters.append(cluster_properties)
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
    session = get_session(session)
    client = session.client("ecs")
    args = deepcopy(kwargs)
    if cluster_name:
        args["cluster"] = cluster_name
    if next_token:
        args["nextToken"] = next_token
    services_r = client.list_services(**args)
    services += services_r["serviceArns"]
    if keyisset("nextToken", services_r):
        return list_all_services(
            cluster_name, services, services_r["nextToken"], session, **args
        )
    return services


def describe_all_services(
    services_list: list, cluster_name=None, session=None, return_as_map=False, **kwargs
):
    """

    :param list[str] services_list:
    :param str cluster_name:
    :param session:
    :param return_as_map:
    :return:
    """
    session = get_session(session)
    client = session.client("ecs")
    chunks = chunked_iterable(services_list, size=10)
    services = []
    if return_as_map:
        services = {}
    for services_chunk in chunks:
        args = deepcopy(kwargs)
        if cluster_name:
            args["cluster"] = cluster_name
        args["services"] = services_chunk
        services_r = client.describe_services(**args)
        for service in services_r["services"]:
            if return_as_map:
                services[service["serviceName"]] = service
            else:
                services.append(service)
    return services


def list_all_task_definitions(definitions=None, next_token=None, ecs_session=None):
    """
    Simple recursive function to list all the task definitions into an account+region.

    :param list definitions:
    :param str next_token:
    :param boto3.session.Session ecs_session:
    :return: list of active task definitions
    :rtype: list
    """
    if ecs_session is None:
        ecs_session = Session()
    client = ecs_session.client("ecs")
    if definitions is None:
        definitions = []
    if next_token:
        defs_r = client.list_task_definitions(nextToken=next_token, status="ACTIVE")
    else:
        defs_r = client.list_task_definitions(status="ACTIVE")
    definitions += defs_r["taskDefinitionArns"]
    if keyisset("nextToken", defs_r):
        return list_all_task_definitions(definitions, defs_r["nextToken"], ecs_session)
    return definitions


def list_container_definitions_images(task_definition, ecs_session=None):
    """
    Simple function to list the images of a given task definition

    :param str task_definition:
    :param boto3.session.Session ecs_session:
    :return: list of images
    :rtype: list
    """
    if ecs_session is None:
        ecs_session = Session()
    client = ecs_session.client("ecs")
    task_def = client.describe_task_definition(
        taskDefinition=task_definition,
        include=[
            "TAGS",
        ],
    )["taskDefinition"]
    images = [container["image"] for container in task_def["containerDefinitions"]]
    return images
