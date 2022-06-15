# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>


import re

PROFILER_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:codeguru-profiler:(?P<region>[a-z\d\-]+-\d):(?P<accountid>\d{12}):"
    r"profilingGroup/(?P<id>\S+)$"
)
