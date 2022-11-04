#!/usr/bin/env python

"""Tests for `compose_x_common` package."""

from os import path

import placebo
import pytest
from boto3.session import Session

from compose_x_common.aws.msk import (
    list_all_kafka_clusters,
    list_all_kafka_clusters_v2,
    list_all_kafka_configurations,
    list_all_kafka_versions,
)

HERE = path.abspath(path.dirname(__file__))


def test_list_all_versions():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/msk/")
    # pill.record()
    pill.playback()
    list_all_kafka_versions(
        session=test_session,
    )


def test_list_all_configurations():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/msk/")
    # pill.record()
    pill.playback()
    list_all_kafka_configurations(
        session=test_session,
    )


def test_list_all_clusters():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/msk/")
    # pill.record()
    pill.playback()
    list_all_kafka_clusters(
        session=test_session,
    )


def test_list_all_clusters_v2():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/msk/")
    # pill.record()
    pill.playback()
    list_all_kafka_clusters_v2(
        session=test_session,
    )
