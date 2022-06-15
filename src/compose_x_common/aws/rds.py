# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>


import re

RDS_DB_INSTANCE_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:rds:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[0-9]{12}):db:(?P<id>[\S]+)$"
)
RDS_DB_CLUSTER_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:rds:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[0-9]{12}):cluster:(?P<id>[\S]+)$"
)

RDS_DB_ID_CLUSTER_ARN_RE = re.compile(
    r"arn:(?:aws|aws-cn|aws-us-gov):rds:(?P<region>[a-z\d\-]+-\d):(?P<accountid>\d{12}):cluster:"
    r"(?P<id>(?!cluster).*?)$"
)
