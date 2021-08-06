#!/usr/bin/env python

"""Tests for `compose_x_common` package."""

from os import path

import placebo
import pytest
from boto3.session import Session

from compose_x_common.aws.ecr import retag_image

HERE = path.abspath(path.dirname(__file__))


def test_image_retag():
    ecr_test_session = Session()
    pill = placebo.attach(ecr_test_session, data_path=f"{HERE}/placebos/ecr/")
    # pill.record()
    pill.playback()
    retag_image(
        "python",
        "3.7",
        "expectedtag",
        delete_old_tag=True,
        ecr_session=ecr_test_session,
    )


def test_missing_image_retag():
    ecr_test_session = Session()
    pill = placebo.attach(ecr_test_session, data_path=f"{HERE}/placebos/ecr/")
    # pill.record()
    pill.playback()
    retag_image(
        "python",
        "3.7",
        "expectedtag",
        delete_old_tag=True,
        ecr_session=ecr_test_session,
    )
