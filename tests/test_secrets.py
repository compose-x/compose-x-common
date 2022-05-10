#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>


import pytest

from compose_x_common.aws.secrets_manager import get_secret_name_from_arn


def test_get_secret_name_from_arn():
    name = get_secret_name_from_arn(
        "arn:aws:secretsmanager:eu-west-1:123456789010:secret:/path/to/secret-p5dd7H"
    )
    assert name == "/path/to/secret"


def test_invalid_secret_arn():
    with pytest.raises(ValueError):
        get_secret_name_from_arn(
            "arn:aws:secretsmanager:eu-west-1:123456789010:secret:/path/to/secret"
        )
