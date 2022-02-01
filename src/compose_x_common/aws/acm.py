#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>
import re

ACM_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:acm:(?P<region>[\S]+):(?P<accountid>[\d]{12}):certificate/"
    r"(?P<id>[a-z0-9]{8}(?:-[a-z0-9]{4}){3}-[a-z0-9]{12})$"
)
