#    -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>


from os import path

import placebo
from boto3.session import Session

from compose_x_common.aws.ecs import (
    CLUSTER_NAME_FROM_ARN,
    describe_all_ecs_clusters,
    describe_all_ecs_clusters_from_ccapi,
    describe_all_services,
    list_all_ecs_clusters,
    list_all_services,
)

HERE = path.abspath(path.dirname(__file__))


def test_list_clusters():
    ecs_test_session = Session()
    pill = placebo.attach(ecs_test_session, data_path=f"{HERE}/placebos/ecs/")
    # pill.record()
    pill.playback()
    clusters = list_all_ecs_clusters(session=ecs_test_session, maxResults=1)
    print(clusters)
    clusters_def = describe_all_ecs_clusters(clusters, session=ecs_test_session)
    clusters_def = describe_all_ecs_clusters(
        clusters, return_as_map=True, session=ecs_test_session
    )
    clusters_def = describe_all_ecs_clusters_from_ccapi(
        clusters, True, True, ecs_test_session
    )
    clusters_def = describe_all_ecs_clusters_from_ccapi(
        clusters, True, False, ecs_test_session
    )
    clusters_def = describe_all_ecs_clusters_from_ccapi(
        clusters, False, True, ecs_test_session
    )


def test_list_services():
    ecs_test_session = Session()
    pill = placebo.attach(ecs_test_session, data_path=f"{HERE}/placebos/ecs/")
    # pill.record()
    pill.playback()
    clusters = list_all_ecs_clusters(session=ecs_test_session)
    cluster_name = CLUSTER_NAME_FROM_ARN.match(clusters[0]).group("name")
    services = list_all_services(cluster_name, session=ecs_test_session, maxResults=1)
    print(services)
    services_def = describe_all_services(
        services, cluster_name, session=ecs_test_session
    )
    print(services_def)


def test_list_no_services():
    ecs_test_session = Session()
    pill = placebo.attach(ecs_test_session, data_path=f"{HERE}/placebos/ecs/")
    # pill.record()
    pill.playback()
    clusters = list_all_ecs_clusters(session=ecs_test_session)
    services = list_all_services(session=ecs_test_session)
    services_def = describe_all_services(
        services,
        return_as_map=True,
        session=ecs_test_session,
    )
    print(services_def)
