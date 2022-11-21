# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""
AWS Glue
"""
import re

GLUE_SR_ARN_RE = re.compile(
    r"^arn:(?P<partition>[\w\-]+):glue:(?P<region>[\w\-]+):"
    r"(?P<accountid>[\d]{12}):registry/"
    r"(?P<id>[\w\-\$\#]{1,255})$"
)

GLUE_SR_NAME_RE = re.compile(r"^[\w\-\$\#]{1,255}$")
