#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>


from os import path

import placebo
from boto3.session import Session

from compose_x_common.aws.acm import (
    find_certificate_from_domain_name,
    list_all_certificates,
)

HERE = path.abspath(path.dirname(__file__))


def test_list_certificates():
    acm_test_session = Session()
    pill = placebo.attach(acm_test_session, data_path=f"{HERE}/placebos/acm/")
    # pill.record()
    pill.playback()
    list_all_certificates(session=acm_test_session, MaxItems=1)


def test_find_certificate():
    acm_test_session = Session()
    pill = placebo.attach(acm_test_session, data_path=f"{HERE}/placebos/acm/")
    # pill.record()
    pill.playback()
    find_certificate_from_domain_name(
        ".demos.lambda-my-aws.io", session=acm_test_session
    )
