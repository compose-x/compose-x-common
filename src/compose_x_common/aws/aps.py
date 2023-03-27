# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2023 John Mille <john@compose-x.io>


"""AWS Managed Prometheus Service"""

import re

APS_WORKSPACE_ARN_RE = re.compile(
    r"arn:(?P<partition>[a-z\d\-]+):aps:(?P<region>[a-z\d\-]+):(?P<accountid>[\d]{12})"
    r":workspace/(?P<id>[a-zA-Z\d\-]+)$"
)
