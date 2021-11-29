#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

import re

SECRET_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:secretsmanager:[\w-]+:[0-9]{12}:secret:"
    r"(?P<id>[\S]+)(?:-[A-Za-z0-9]{6,})$"
)
