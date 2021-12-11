#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

import re

NEPTUNE_DB_CLUSTER_ARN_RE = re.compile(
    r"^arn:aws(?:us-gov|-cn)?:rds:(?P<region>[a-z0-9-]+):(?P<accountid>[0-9]{12}):cluster:(?P<id>[\S]+)$"
)

NEPTUNE_DB_RESOURCES_ARN_RE = re.compile(
    r"^arn:aws(?:us-gov|-cn)?:neptune-db:(?P<region>[a-z0-9-]+):(?P<accountid>[0-9]{12}):cluster:(?P<id>[\S]+)$"
)
