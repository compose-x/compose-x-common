#    -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

from copy import deepcopy

from boto3.session import Session

from compose_x_common.compose_x_common import keyisset

from . import get_session


def list_all_scalable_targets(
    namespace=None, targets=None, next_token=None, session=None, **kwargs
):
    """

    :param str namespace: Required parameter
    :param targets:
    :param next_token:
    :param session:
    :param kwargs:
    :return:
    """
    if targets is None:
        targets = []
    session = get_session(session)
    client = session.client("application-autoscaling")
    args = deepcopy(kwargs)
    if not namespace and not keyisset("ServiceNamespace", args):
        raise KeyError(
            "ServiceNamespace must be set either via `namespace` or `kwargs['ServiceNamespace']`"
        )
    if not keyisset("ServiceNamespace", args):
        args["ServiceNamespace"] = namespace
    if next_token:
        args["NextToken"] = next_token
    targets_r = client.describe_scalable_targets(**args)
    if keyisset("NextToken", targets_r):
        return list_all_scalable_targets(
            targets, targets_r["NextToken"], session, **args
        )
    targets += targets_r["ScalableTargets"]
    return targets
