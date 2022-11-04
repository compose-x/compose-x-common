# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>


from copy import deepcopy

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset, set_else_none

SCHEDULED_ACTION_ARN_RE = (
    r"arn:aws(?:[a-z\-]+)?:autoscaling:(?P<region>[\w-]+):"
    r"(?P<accountid>\d{12}):scheduledAction:(?P<id>[\S]+)"
)


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
    namespace = set_else_none("ServiceNamespace", kwargs, namespace)
    if namespace is None:
        raise KeyError(
            "ServiceNamespace must be set either via `namespace` or `kwargs['ServiceNamespace']`"
        )
    args["ServiceNamespace"] = namespace
    if next_token:
        args["NextToken"] = next_token
    targets_r = client.describe_scalable_targets(**args)
    targets += targets_r["ScalableTargets"]
    if keyisset("NextToken", targets_r):
        args.update({"NextToken": targets_r["NextToken"]})
        return list_all_scalable_targets(
            namespace,
            targets=targets,
            next_token=targets_r["NextToken"],
            session=session,
            **args
        )
    return targets
