#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2022 John Mille <john@compose-x.io>

import pytest

from compose_x_common.aws.arns import ARNS_PER_CFN_TYPE


@pytest.fixture
def valid_arns():
    return {
        "AWS::IAM::Role": "arn:aws:iam::965889391954:role/build-docker-python-CodeBuildRole",
        "AWS::EC2::VPC": "arn:aws:ec2:eu-west-1:123456789010:vpc/vpc-abcd1234",
        "AWS::EC2::Subnet": "arn:aws:ec2:eu-west-1:123456789010:subnet/subnet-abcd1234",
        "AWS::SQS::Queue": "arn:aws:sqs:eu-west-1:123456789010:abcd",
        "AWS::SNS::Topic": "arn:aws:sns:eu-west-1:123456789010:abcd",
        "AWS::RDS::Cluster": "arn:aws:rds:eu-west-1:123456789010:cluster:database-2",
        "AWS::RDS::Instance": "arn:aws:rds:eu-west-1:123456789010:db:instance",
        "AWS::SecretsManager::Secret": "arn:aws:secretsmanager:eu-west-1:123456789010:secret:/path/to/secret-p5dd7H",
        "AWS::SSM::Parameter": "arn:aws:ssm:eu-west-1:123456789010:parameter/Dev/ProductConsumer/Kafka/PdsTopic",
        "AWS::Elasticsearch::Domain": "arn:aws:es:eu-west-1:123456789010:domain/domain-2",
        "AWS::OpenSearchService::Domain": "arn:aws:es:eu-west-1:123456789010:domain/domain-2",
        "AWS::KMS::Key": "arn:aws:kms:eu-west-1:123456789010:key/b8aa5596-8746-4da6-9b58-2f44aa566d9e",
        "AWS::KMS::Alias": "arn:aws:kms:eu-west-1:123456789010:alias/some/alias",
        "AWS::Kinesis::Stream": "arn:aws:kinesis:eu-west-1:123456789010:stream/some-stream",
        "AWS::DynamoDB::Table": "arn:aws:dynamodb:eu-west-1:123456789010:table/some-table",
        "AWS::S3::Bucket": "arn:aws:s3:::s3-bucket-name",
        "AWS::CertificateManager::Certificate": "arn:aws:acm:eu-west-1:123456789010:certificate/fc2017aa-797a-4051-9cc6-876c91dd83e5",
        "AWS::Neptune::DBCluster": "arn:aws:rds:eu-west-1:123456789010:cluster:neptune-graph",
        "AWS::ServiceDiscovery::PrivateDnsNamespace": "arn:aws:servicediscovery:eu-west-1:123456789010:namespace/ns-s7wyohfj7m5pfgg7",
        "AWS::ServiceDiscovery::PublicDnsNamespace": "arn:aws:servicediscovery:eu-west-1:123456789010:namespace/ns-s7wyohfj7m5pfgg7",
        "AWS::ServiceDiscovery::HttpNamespace": "arn:aws:servicediscovery:eu-west-1:123456789010:namespace/ns-s7wyohfj7m5pfgg7",
        "AWS::ECS::Cluster": "arn:aws:ecs:eu-west-1:123456789010:cluster/default",
        "AWS::KinesisFirehose::DeliveryStream": "arn:aws:firehose:eu-west-1:123456789010:deliverystream/PUT-S3-g6B0t",
        "AWS::Route53::HostedZone": "arn:aws:route53:::hostedzone/Z0511212EJ09VUT1A6P1",
        "AWS::ECS::Service": "arn:aws:ecs:eu-west-1:123456789010:service/prod/connect-cluster",
        "AWS::MSK::Cluster": "arn:aws:kafka:us-east-1:123456789012:cluster/CustomerMessages/abcd1234-abcd-dcba-4321-a1b2abcd9f9f-2",
        "AWS::MSK::ServerlessCluster": "arn:aws:kafka:eu-west-1:123456789012:cluster/demo-cluster-1/d7e68213-0896-4839-80df-dea01b79750c-s1",
        "AWS::MSK::Configuration": "arn:aws:kafka:eu-west-1:123456789012:configuration/default-msk-331/e44a32b9-4cba-4686-a1e4-b0e72fb1baa4-8",
        "AWS::Glue::Registry": "arn:aws:glue:us-east-2:012345678912:registry/registryname-1",
        "AWS::WAFv2::WebACL": "arn:aws:wafv2:eu-west-1:012345678912:regional/webacl/wafv2-webacl-dev/732c1718-ea9f-4370-a2a9-607f948a3cd7",
        "AWS::EFS::FileSystem": "arn:aws:elasticfilesystem:eu-west-1:108833517019:file-system/fs-08a8676339b99dc0a",
    }


def test_valid_arns(valid_arns):
    for aws_type, regexp in ARNS_PER_CFN_TYPE.items():
        if aws_type not in valid_arns:
            print("Untested", aws_type)
            continue
        groups = regexp.match(valid_arns[aws_type])
        try:
            assert groups and groups.group("id")
        except AssertionError:
            raise AssertionError(
                "ARN validation failed for",
                aws_type,
                valid_arns[aws_type],
                regexp.pattern,
            )
