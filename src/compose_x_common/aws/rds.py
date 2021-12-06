#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

import re

RDS_DB_INSTANCE_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:rds:[\w-]+:(?P<accountid>[0-9]{12}):db:(?P<id>[\S]+)$"
)
RDS_DB_CLUSTER_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:rds:[\w-]+:(?P<accountid>[0-9]{12}):cluster:(?P<id>[\S]+)$"
)

RDS_DB_ID_CLUSTER_ARN_RE = re.compile(
    r"arn:(?:aws|aws-cn|aws-us-gov):rds:(?:[a-z0-9-]+):\d{12}:cluster:"
    r"(?P<id>(?!cluster).*?)$"
)
