#    -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>


from os import path

import placebo
from boto3.session import Session

from compose_x_common.aws.application_autoscaling import list_all_scalable_targets

HERE = path.abspath(path.dirname(__file__))


def test_list_scalable_targets():

    test_session = Session()
    pill = placebo.attach(test_session, data_path=f"{HERE}/placebos/appas/")
    # pill.record()
    pill.playback()
    clusters = list_all_scalable_targets("ecs", session=test_session)
