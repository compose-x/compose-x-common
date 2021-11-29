#!/usr/bin/env python

"""Tests for `compose_x_common` package."""

from os import path

import placebo
import pytest
from boto3.session import Session

from compose_x_common.aws import get_account_id, get_region_azs, validate_iam_role_arn

HERE = path.abspath(path.dirname(__file__))


def test_get_regions():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/common/")
    # pill.record()
    pill.playback()
    get_region_azs(test_session)


def test_get_account_id():
    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/common/")
    # pill.record()
    pill.playback()
    get_account_id(test_session)


def test_valid_role_arn():
    role_arn = "arn:aws:iam::012345678912:role/an-iam-role"
    validate_iam_role_arn(role_arn)


def test_invalid_role_arn():
    role_arns = [
        "arn:aws:iam::acdp45678912:role/an-iam-role",
        "arn:aws:iam::012345678912:policy/an-iam-role",
        "arn:aws:iam:eu-west-1:12345678912:role/an-iam-role",
    ]
    for role in role_arns:
        with pytest.raises(ValueError):
            validate_iam_role_arn(role)
