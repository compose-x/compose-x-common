# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

import re

ACM_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:acm:(?P<region>[a-z\d\-]+-\d):(?P<accountid>\d{12}):"
    r"certificate/(?P<id>[a-z\d]{8}(?:-[a-z\d]{4}){3}-[a-z\d]{12})$"
)
