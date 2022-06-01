# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>


import re

IAM_ROLE_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:iam::(?P<account>[0-9]{12}):role/(?P<id>[\S]+)$"
)
IAM_USER_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:iam::(?P<account>[0-9]{12}):user/(?P<id>[\S]+)$"
)
