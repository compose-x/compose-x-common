#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>

from .acm import ACM_ARN_RE
from .cloudmap import NAMESPACE_ARN_RE
from .codeguru_profiler import PROFILER_ARN_RE
from .cognito_userpool import USER_POOL_RE
from .dynamodb import TABLE_ARN_RE
from .elasticache import CACHE_CLUSTER_ARN_RE
from .kinesis import KINESIS_STREAM_ARN_RE
from .kms import KMS_ALIAS_ARN_RE, KMS_KEY_ARN_RE
from .neptune import NEPTUNE_DB_CLUSTER_ARN_RE
from .opensearch import OS_DOMAIN_ARN_RE
from .rds import RDS_DB_CLUSTER_ARN_RE, RDS_DB_INSTANCE_ARN_RE
from .s3 import S3_BUCKET_ARN_RE
from .secrets_manager import SECRET_ARN_RE
from .sns import SNS_TOPIC_ARN_RE
from .sqs import SQS_QUEUE_ARN_RE
from .ssm_parameter import SSM_PARAMETER_ARN_RE
from .vpc import SUBNET_ARN_RE, VPC_ARN_RE

ARNS_PER_CFN_TYPE = {
    "AWS::EC2::VPC": VPC_ARN_RE,
    "AWS::EC2::Subnet": SUBNET_ARN_RE,
    "AWS::SQS::Queue": SQS_QUEUE_ARN_RE,
    "AWS::SNS::Topic": SNS_TOPIC_ARN_RE,
    "AWS::RDS::Cluster": RDS_DB_CLUSTER_ARN_RE,
    "AWS::RDS::Instance": RDS_DB_INSTANCE_ARN_RE,
    "AWS::SecretsManager::Secret": SECRET_ARN_RE,
    "AWS::SSM::Parameter": SSM_PARAMETER_ARN_RE,
    "AWS::Elasticsearch::Domain": OS_DOMAIN_ARN_RE,
    "AWS::OpenSearchService::Domain": OS_DOMAIN_ARN_RE,
    "AWS::KMS::Key": KMS_KEY_ARN_RE,
    "AWS::KMS::Alias": KMS_ALIAS_ARN_RE,
    "AWS::Kinesis::Stream": KINESIS_STREAM_ARN_RE,
    "AWS::DynamoDB::Table": TABLE_ARN_RE,
    "AWS::S3::Bucket": S3_BUCKET_ARN_RE,
    "AWS::CodeGuruProfiler::ProfilingGroup": PROFILER_ARN_RE,
    "AWS::CertificateManager::Certificate": ACM_ARN_RE,
    "AWS::Cognito::UserPool": USER_POOL_RE,
    "AWS::ElastiCache::CacheCluster": CACHE_CLUSTER_ARN_RE,
    "AWS::Neptune::DBCluster": NEPTUNE_DB_CLUSTER_ARN_RE,
    "AWS::ServiceDiscovery::PrivateDnsNamespace": NAMESPACE_ARN_RE,
    "AWS::ServiceDiscovery::PublicDnsNamespace": NAMESPACE_ARN_RE,
    "AWS::ServiceDiscovery::HttpNamespace": NAMESPACE_ARN_RE,
}

ARNS_PER_TAGGINGAPI_TYPE = {
    "ec2:vpc": VPC_ARN_RE,
    "ec2:subnet": SUBNET_ARN_RE,
    "sqs": SQS_QUEUE_ARN_RE,
    "sns": SNS_TOPIC_ARN_RE,
    "rds:cluster": RDS_DB_CLUSTER_ARN_RE,
    "rds:instance": RDS_DB_INSTANCE_ARN_RE,
    "secretsmanager:secret": SECRET_ARN_RE,
    "ssm:parameter": SSM_PARAMETER_ARN_RE,
    "es:domain": OS_DOMAIN_ARN_RE,
    "kms:key": KMS_KEY_ARN_RE,
    "kms:alias": KMS_ALIAS_ARN_RE,
    "kinesis:stream": KINESIS_STREAM_ARN_RE,
    "dynamodb:table": TABLE_ARN_RE,
    "s3": S3_BUCKET_ARN_RE,
    "codeguru-profiler": PROFILER_ARN_RE,
    "acm:certificate": ACM_ARN_RE,
    "cognito-idp": USER_POOL_RE,
    "elasticache:cluster": CACHE_CLUSTER_ARN_RE,
}
