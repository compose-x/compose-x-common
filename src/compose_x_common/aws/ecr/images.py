# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""
Functions to help with images in ECR manipulation
"""

from __future__ import annotations

from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import chunked_iterable, keyisset


def list_all_images(
    repo_name: str,
    images: list = None,
    next_token: str = None,
    ecr_session: Session = None,
    **kwargs,
) -> list:
    """
    Retrieves all the images of a given repository

    :param str repo_name:
    :param images:
    :param next_token:
    :param boto3.session.Session ecr_session:
    :return:
    """
    session = get_session(ecr_session)
    client = session.client("ecr")
    if images is None:
        images = []
    args = {
        "maxResults": 42,
        "repositoryName": repo_name,
        "filter": {"tagStatus": "ANY"},
    }
    args.update(kwargs)
    if not next_token:
        res = client.list_images(**args)
    else:
        args.update({"nextToken": next_token})
        res = client.list_images(**args)
    images += res["imageIds"]
    if "nextToken" in res.keys() and res["nextToken"]:
        return list_all_images(
            repo_name,
            images=images,
            next_token=res["nextToken"],
            ecr_session=session,
            **kwargs,
        )
    return images


def get_docker_image_details(
    repostory_name: str,
    image_tag: str,
    image_digest: str = None,
    registry_id: str = None,
    session: Session = None,
):
    """
    Function to retrieve the image information
    """
    session = get_session(session)
    client = session.client("ecr")
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


def get_all_images_details(
    repo_name: str,
    registry_id: str = None,
    ecr_session: Session = None,
) -> list:
    session = get_session(ecr_session)
    if registry_id is None:
        registry_id = session.client("sts").get_caller_identity()["Account"]
    repo_images = list_all_images(repo_name, ecr_session=session)
    images_details = []
    client = session.client("ecr")
    for images in chunked_iterable(repo_images, 10):
        images_details_r = client.batch_get_image(
            registryId=registry_id,
            repositoryName=repo_name,
            imageIds=images,
        )
        if keyisset("images", images_details_r):
            images_details += images_details_r["images"]
    return images_details


def retag_image(
    repostory_name: str,
    new_tag: str,
    image_tag: str,
    image_digest: str = None,
    delete_old_tag: str = True,
    registry_id: str = None,
    session: Session = None,
):
    """
    Function to rename an image in ECR via API call

    :param repostory_name: ECR Repository name
    :param str new_tag: The new tag for the image
    :param bool delete_old_tag: Whether or no to keep the tag for the image
    :param str image_digest: The image digest (sha)
    :param str image_tag: The image
    :param boto3.session.Session session:
    """
    session = get_session(session)
    if registry_id is None:
        registry_id = session.client("sts").get_caller_identity()["Account"]
    print(f"Registry ID set to {registry_id}")
    client = session.client("ecr")
    images = get_docker_image_details(
        repostory_name, image_tag, image_digest, registry_id, session
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
