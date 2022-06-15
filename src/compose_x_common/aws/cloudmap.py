# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

import re

NAMESPACE_ARN_RE = re.compile(
    r"^arn:aws(?:\w+)?:servicediscovery:(?P<region>[a-z\d\-]+-\d):(?P<accountid>\d{12}):"
    r"namespace/(?P<id>ns-[a-zA-Z\d]+)$"
)


def get_all_dns_namespaces(session, namespaces=None, next_token=None):
    """
    Function to recursively fetch all namespaces in account

    :param list namespaces:
    :param boto3.session.Session session:
    :param str next_token:
    :return:
    """
    if namespaces is None:
        namespaces = []
    filters = [{"Name": "TYPE", "Values": ["DNS_PRIVATE"], "Condition": "EQ"}]
    client = session.client("servicediscovery")
    if not next_token:
        namespaces_r = client.list_namespaces(Filters=filters)
    else:
        namespaces_r = client.list_namespaces(Filters=filters, NextToken=next_token)
    namespaces += namespaces_r["Namespaces"]
    if "NextToken" in namespaces_r:
        return get_all_dns_namespaces(session, namespaces, namespaces_r["NextToken"])
    return namespaces
