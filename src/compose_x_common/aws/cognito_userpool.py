# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>


import re

USER_POOL_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:cognito-idp:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[\d]{12}):userpool/(?P<id>[\S]+)$"
)
