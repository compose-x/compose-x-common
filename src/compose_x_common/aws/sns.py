# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

import re
from typing import Union

from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset

SNS_TOPIC_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z\-]+)?:sns:(?P<region>[a-z\d\-]+-\d):(?P<accountid>[0-9]{12}):(?P<id>[\S]+)$"
)


def list_all_topics(
    topics: list = None, next_token: str = None, session: Session = None
) -> list:
    session = get_session(session)
    if topics is None:
        topics: list = []
    if not next_token:
        topics_r = session.client("sns").list_topics()
    else:
        topics_r = session.client("sns").list_topics(NextToken=next_token)
    topics += topics_r["Topics"]
    if keyisset("NextToken", topics_r):
        return list_all_topics(topics, topics_r["NextToken"], session)
    return topics


def describe_all_topics(
    topics_arn: list = None, session: Session = None, as_mapping: bool = False
) -> Union[list, dict]:
    session = get_session(session)
    client = session.client("sns")
    if not topics_arn:
        topics_arn = [_topic["TopicArn"] for _topic in list_all_topics()]
    if as_mapping:
        topics_attrs: dict = {}
        for topic_arn in topics_arn:
            topics_attrs[topic_arn] = client.get_topic_attributes(TopicArn=topic_arn)
    else:
        topics_attrs: list = []
        for topic_arn in topics_arn:
            topics_attrs.append(client.get_topic_attributes(TopicArn=topic_arn))
    return topics_attrs
