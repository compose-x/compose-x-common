# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2024 John Mille <john@compose-x.io>

"""ELB Helper functions"""

import re

LB_V2_LB_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:elasticloadbalancing:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[\d]{12}):"
    r"loadbalancer/(?P<type>net|app)/(?P<id>[\S]+)$"
)

LB_V2_LISTENER_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:elasticloadbalancing:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[\d]{12}):"
    r"listener/(?P<type>net|app)/(?P<id>[\S]+)$"
)

LB_V2_LISTENER_RULE_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:elasticloadbalancing:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[\d]{12}):"
    r"listener-rule/(?P<type>net|app)/(?P<id>[\S]+)$"
)

LB_V2_TGT_GROUP_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:elasticloadbalancing:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[\d]{12}):"
    r"targetgroup/(?P<id>[\S]+)$"
)
