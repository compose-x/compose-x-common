# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2024 John Mille <john@compose-x.io>

"""AWS::WAFv2::"""

import re

WAF_V2_WEB_ACL_ARN_RE = re.compile(
    r"^arn:aws(?P<partition>-[a-z]+)?:wafv2:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[\d]{12}):"
    r"(?P<scope>regional|global)/webacl/(?P<name>[\w\-_]+)/(?P<id>[\S]+)$"
)

WAF_V2_WEB_ACL_REF_RE = re.compile(
    r"^(?P<name>[\w\-_]+)\|(?P<id>[\w\-]+)\|(?P<scope>REGIONAL|GLOBAL)$"
)
WAF_V2_WEB_ACL_NAMESPACE_PREFIX_RE = re.compile(
    r"^awswaf:\d{12}:webacl:(?P<name>[\w\-_]+):"
)
