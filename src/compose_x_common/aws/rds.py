#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

import re

RDS_DB_INSTANCE_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:rds:[\w-]+:[0-9]{12}:db:(?P<id>[\S]+)$"
)
RDS_DB_CLUSTER_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:rds:[\w-]+:[0-9]{12}:cluster:(?P<id>[\S]+)$"
)
