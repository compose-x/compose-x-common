#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

import re

PROFILER_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:codeguru-profiler:"
    r"(?P<region>[\S]+):[0-9]{12}:profilingGroup/(?P<id>[\S]+)$"
)
