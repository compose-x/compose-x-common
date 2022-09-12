# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

"""
Module to help with Route53 management
"""

from __future__ import annotations

import re

from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset

ZONEID_RE = re.compile(r"^Z[A-Z0-9]{3,255}$")
ZONE_ARN_NE = re.compile(r"arn:aws:route53:::hostedzone/(?P<id>Z[A-Z0-9]{3,255})$")
ZONE_CHANGE_RE = re.compile(r"arn:aws:route53:::change/(?P<id>[A-Z0-9]+)$")


def list_all_hosted_zones(
    zones: list = None, next_token: str = None, session: Session = None, **kwargs
) -> list:
    session = get_session(session)
    if zones is None:
        zones = []
    if not next_token:
        zones_r = session.client("route53").list_hosted_zones(**kwargs)
    else:
        zones_r = session.client("route53").list_hosted_zones(
            Marker=next_token, **kwargs
        )
    zones += zones_r["HostedZones"]
    if keyisset("NextMarker", zones_r):
        return list_all_hosted_zones(zones, zones_r["NextMarker"], session, **kwargs)
    return zones


def list_all_records(
    zone_id: str,
    records: list = None,
    next_record: str = None,
    next_record_type: str = None,
    session: Session = None,
    **kwargs,
) -> list:
    session = get_session(session)
    if records is None:
        records = []
    if next_record and next_record_type:
        records_r = session.client("route53").list_resource_record_sets(
            HostedZoneId=zone_id,
            StartRecordName=next_record,
            StartRecordType=next_record_type,
            **kwargs,
        )
    else:
        records_r = session.client("route53").list_resource_record_sets(
            HostedZoneId=zone_id, **kwargs
        )
    records += records_r["ResourceRecordSets"]
    if keyisset("IsTruncated", records_r):
        return list_all_records(
            zone_id,
            records,
            next_record=records_r["NextRecordName"],
            next_record_type=records_r["NextRecordType"],
            session=session,
            **kwargs,
        )
    return records
