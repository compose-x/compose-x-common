#!/usr/bin/env python

"""Tests for `compose_x_common` package."""

from os import path

import placebo
import pytest
from boto3.session import Session

from compose_x_common.aws.ecr.images import (
    get_all_images_details,
    list_all_images,
    retag_image,
)
from compose_x_common.aws.ecr.repositories import (
    filter_repos_from_regexp,
    list_ecr_repos,
)

HERE = path.abspath(path.dirname(__file__))


def test_image_retag():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/ecr/")
    # pill.record()
    pill.playback()
    retag_image(
        "python",
        "3.7",
        "expectedtag",
        delete_old_tag=True,
        session=test_session,
    )


def test_missing_image_retag():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/ecr/")
    # pill.record()
    pill.playback()
    retag_image(
        "python",
        "3.7",
        "expectedtag",
        delete_old_tag=True,
        session=test_session,
    )


def test_list_all_images():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/ecr/")
    # pill.record()
    pill.playback()
    images = list_all_images(
        "confluentinc/cp-kafka-connect", ecr_session=test_session, maxResults=5
    )
    assert len(images) == 11


def test_get_all_images_details():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/ecr/get_all_images")
    # pill.record()
    pill.playback()
    images = get_all_images_details(
        "confluentinc/cp-kafka-connect", ecr_session=test_session
    )


def test_list_all_repositories():
    test_session = Session()
    pill = placebo.attach(
        test_session, data_path=f"{HERE}/placebos/ecr/repos/list_all_repositories"
    )
    # pill.record()
    pill.playback()
    images = list_ecr_repos(ecr_session=test_session, maxResults=2)


def test_filter_repositories():
    test_session = Session()
    pill = placebo.attach(
        test_session, data_path=f"{HERE}/placebos/ecr/repos/filter_repositories"
    )
    # pill.record()
    pill.playback()
    images = filter_repos_from_regexp(
        list_ecr_repos(ecr_session=test_session), "blog-app"
    )
    assert images == ["blog-app01", "blog-app02"]
