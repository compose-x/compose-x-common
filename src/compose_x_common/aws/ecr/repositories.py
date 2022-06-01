# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

from __future__ import annotations

import re

from boto3.session import Session

from compose_x_common.aws import get_session

"""
Functions to help with repositories in ECR manipulation
"""

DEFAULT_REGEXP = re.compile(r"^.*$")


def list_ecr_repos(
    repos: list = None, next_token: str = None, ecr_session: Session = None, **kwargs
):
    """
    Function to retrieve all the ECR repositories

    :param repos:
    :param next_token:
    :param boto3.session.Session ecr_session:
    :return:
    """
    if repos is None:
        repos = []
    ecr_session = get_session(ecr_session)
    client = ecr_session.client("ecr")
    args = {
        "maxResults": 42,
    }
    args.update(kwargs)
    if not next_token:
        res = client.describe_repositories(**args)
    else:
        args["nextToken"] = next_token
        res = client.describe_repositories(**args)
    repos += res["repositories"]
    if "nextToken" in res and res["nextToken"]:
        return list_ecr_repos(
            repos=repos, next_token=res["nextToken"], ecr_session=ecr_session, **kwargs
        )
    return repos


def filter_repos_from_regexp(repos_list: list, repos_names_filter: str = None):
    """
    Function to filter repositories based their name and a regular expression

    :param repos_list:
    :param repos_names_filter:
    :return:
    """
    filtered_repos = []
    if repos_names_filter and isinstance(repos_names_filter, str):
        repos_filter = re.compile(repos_names_filter)
    else:
        repos_filter = DEFAULT_REGEXP
    for repo in repos_list:
        if isinstance(repo, dict):
            if "repositoryName" not in repo.keys():
                raise KeyError("Missing repository name from ")
            repo_name = repo["repositoryName"]
        elif isinstance(repo, str):
            repo_name = repo
        else:
            raise TypeError(
                "The repo list must be a list of dicts or str. Got", type(repo)
            )
        if repos_filter.match(repo_name):
            filtered_repos.append(repo_name)
    return filtered_repos
