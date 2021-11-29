#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>


from boto3.session import Session


def get_resources_from_tags(aws_resource_search, search_tags, session=None):
    """

    :param boto3.session.Session session: The boto3 session for API calls
    :param str aws_resource_search: AWS Service short code, ie. rds, ec2
    :param list search_tags: The tags to search the resource with.
    :return:
    """
    if session is None:
        session = Session()
    client = session.client("resourcegroupstaggingapi")
    resources_r = client.get_resources(
        ResourceTypeFilters=[aws_resource_search], TagFilters=search_tags
    )
    return resources_r
