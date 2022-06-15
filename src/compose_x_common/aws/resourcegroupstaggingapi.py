# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

from compose_x_common.aws import get_session
from compose_x_common.aws.arns import ARNS_PER_TAGGINGAPI_TYPE
from compose_x_common.compose_x_common import keyisset


def get_resources_from_tags(aws_resource_search, search_tags, session=None):
    """

    :param boto3.session.Session session: The boto3 session for API calls
    :param str aws_resource_search: AWS Service short code, ie. rds, ec2
    :param list search_tags: The tags to search the resource with.
    :return:
    """
    session = get_session(session)
    client = session.client("resourcegroupstaggingapi")
    resources_r = client.get_resources(
        ResourceTypeFilters=[aws_resource_search], TagFilters=search_tags
    )
    return resources_r


def find_aws_resource_arn_from_tags_api(
    aws_resource_search, search_tags, allow_multi=False, session=None
):
    """
    Function to find the RDS DB based on info

    :param list search_tags:
    :param str aws_resource_search: Resource type we are after within the AWS Service, ie. cluster, instance
    :param bool allow_multi: Allows more than one AWS resource to be found at a time with the given tags.
    :param boto3.session.Session session: Boto3 session for clients
    :return: The list of ARNs
    :rtype: list
    """
    session = get_session(session)
    resources_r = get_resources_from_tags(
        aws_resource_search, search_tags, session=session
    )

    if not keyisset("ResourceTagMappingList", resources_r):
        raise LookupError(
            "No resources were found with the provided tags and information",
            aws_resource_search,
        )

    if aws_resource_search in ARNS_PER_TAGGINGAPI_TYPE.keys():
        match_exp = ARNS_PER_TAGGINGAPI_TYPE[aws_resource_search]
        arns = [
            _["ResourceARN"]
            for _ in resources_r["ResourceTagMappingList"]
            if match_exp.match(_["ResourceARN"])
        ]
    else:
        arns = [_["ResourceARN"] for _ in resources_r["ResourceTagMappingList"]]

    if len(arns) == 1:
        return arns
    elif not allow_multi and len(arns) > 1:
        raise LookupError(
            f"More than one resource {aws_resource_search} were found with the current tags.",
            search_tags,
            "Found",
            arns,
        )
    elif allow_multi and len(arns) > 1:
        return arns
