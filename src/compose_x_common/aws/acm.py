# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2022 John Mille <john@compose-x.io>

import re

from boto3.session import Session

from compose_x_common.aws import get_session
from compose_x_common.compose_x_common import keyisset, set_else_none

ACM_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:acm:(?P<region>[a-z\d\-]+-\d):(?P<accountid>\d{12}):"
    r"certificate/(?P<id>[a-z\d]{8}(?:-[a-z\d]{4}){3}-[a-z\d]{12})$"
)


def list_all_certificates(
    certs: list = None, next_token: str = None, session: Session = None, **kwargs
) -> list:
    if certs is None:
        certs: list = []
    session = get_session(session)
    client = session.client("acm")
    if next_token:
        certs_r = client.list_certificates(NextToken=next_token, **kwargs)
    else:
        certs_r = client.list_certificates(**kwargs)
    certs += certs_r["CertificateSummaryList"]
    if keyisset("NextToken", certs_r):
        return list_all_certificates(
            certs, next_token=certs_r["NextToken"], session=session, **kwargs
        )
    return certs


def find_certificate_from_domain_name(
    domain_name: str, include_subjects_alt: bool = False, session: Session = None
):
    session = get_session(session)
    all_certs = list_all_certificates(session=session)
    client = session.client("acm")
    for cert in all_certs:
        if cert["DomainName"] == domain_name:
            return client.describe_certificate(CertificateArn=cert["CertificateArn"])[
                "Certificate"
            ]
        elif include_subjects_alt:
            certificate_r = client.describe_certificate(
                CertificateArn=cert["CertificateArn"]
            )["Certificate"]
            alt_subjects = set_else_none("SubjectAlternativeNames", certificate_r)
            if domain_name in alt_subjects:
                return certificate_r
    return None
