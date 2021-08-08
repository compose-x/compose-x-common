#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@compose-x.io>

import re

from boto3.session import Session

from compose_x_common.compose_x_common import keyisset

PRIVATE_ECR_URI_RE = re.compile(
    r"(?P<account_id>\d{12}).dkr.ecr.(?P<region>[a-z0-9-]+).amazonaws.com/"
    r"(?P<repo_name>[a-zA-Z0-9-_./]+)(?P<tag>(?:\@sha[\d]+:[a-z-Z0-9]+$)|(?::[\S]+$))"
)


def get_docker_image_details(
    repostory_name,
    image_tag,
    image_digest=None,
    registry_id=None,
    ecr_session=None,
):
    """
    Function to retrive the image information
    :return:
    """
    if not ecr_session:
        ecr_session = Session()
    client = ecr_session.client("ecr")
    image_q = {}
    if not image_digest and not image_tag:
        raise KeyError("You must specify at least one of image_digest or image_tag")
    if image_digest:
        image_q["imageDigest"] = image_digest
    if image_tag:
        image_q["imageTag"] = image_tag
    image_manifest_r = client.batch_get_image(
        registryId=registry_id,
        repositoryName=repostory_name,
        imageIds=[
            image_q,
        ],
    )
    if not keyisset("images", image_manifest_r) and keyisset(
        "failures", image_manifest_r
    ):
        print(image_manifest_r["failures"])
        return None
    return image_manifest_r["images"]


def retag_image(
    repostory_name,
    new_tag,
    image_tag,
    image_digest=None,
    delete_old_tag=True,
    registry_id=None,
    ecr_session=None,
):
    """
    Function to rename an image in ECR via API call

    :param repostory_name: ECR Repository name
    :param str new_tag: The new tag for the image
    :param bool delete_old_tag: Whether or no to keep the tag for the image
    :param str image_digest: The image digest (sha)
    :param str image_tag: The image
    :param boto3.session.Session ecr_session:
    """
    if not ecr_session:
        ecr_session = Session()
    if registry_id is None:
        registry_id = ecr_session.client("sts").get_caller_identity()["Account"]
    print(f"Registry ID set to {registry_id}")
    client = ecr_session.client("ecr")
    images = get_docker_image_details(
        repostory_name, image_tag, image_digest, registry_id, ecr_session
    )
    if not images:
        print("No images found. Skipping")
        return None
    if len(images) > 1:
        print("Only one image expected to rename. Skipping")
        return None
    image = images[0]
    client.put_image(
        registryId=registry_id,
        repositoryName=repostory_name,
        imageManifest=image["imageManifest"],
        imageManifestMediaType=image["imageManifestMediaType"],
        imageTag=new_tag,
        imageDigest=image["imageId"]["imageDigest"],
    )
    if delete_old_tag:
        client.batch_delete_image(
            registryId=registry_id,
            repositoryName=repostory_name,
            imageIds=[image["imageId"]],
        )
