#!/usr/bin/env python

"""Tests for `compose_x_common` package."""

from os import path

import placebo
import pytest
from boto3.session import Session

from compose_x_common.aws.kms import get_key_from_alias, list_all_aliases, list_all_keys

HERE = path.abspath(path.dirname(__file__))


def test_image_retag():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/kms/")
    # pill.record()
    pill.playback()
    list_all_keys(
        session=test_session,
    )


def test_missing_image_retag():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/kms/")
    # pill.record()
    pill.playback()
    list_all_aliases(
        session=test_session,
    )


def test_get_key_from_alias():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/kms/")
    # pill.record()
    pill.playback()
    key = get_key_from_alias("alias/aws/s3", session=test_session)
    assert "KeyArn" in key.keys()
