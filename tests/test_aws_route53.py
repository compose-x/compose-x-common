#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

from os import path

import placebo
from boto3.session import Session

from compose_x_common.aws.route53 import list_all_hosted_zones, list_all_records

HERE = path.abspath(path.dirname(__file__))


def test_route53():
    session = Session()
    pill = placebo.attach(session, data_path=f"{HERE}/placebos/route53/")
    pill.record()
    # pill.playback()
    _zones = list_all_hosted_zones(session=session, MaxItems="1")
    assert len(_zones) == 3
    _records = list_all_records(_zones[0]["Id"], session=session, MaxItems="5")
    assert len(_records) == 12
