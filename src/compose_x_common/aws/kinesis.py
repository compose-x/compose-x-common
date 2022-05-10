# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@compose-x.io>


import re

KINESIS_STREAM_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:kinesis:[\S]+:(?P<accountid>[0-9]{12}):stream/(?P<id>[\S]+)$"
)

KINESIS_FIREHOSE_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:firehose:(?P<region>[\S]+):(?P<accountid>[0-9]{12}):deliverystream/(?P<id>[\S]+)$"
)
