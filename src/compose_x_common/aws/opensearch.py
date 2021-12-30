#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

import re

OS_DOMAIN_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:es:[\w-]+:(?P<accountid>[0-9]{12}):domain/(?P<id>[\S]+)$"
)
