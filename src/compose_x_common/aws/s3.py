# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

import re

S3_BUCKET_ARN_RE = re.compile(r"^arn:aws(?:-[a-z]+)?:s3:::(?P<id>[\w\-.]+)$")
