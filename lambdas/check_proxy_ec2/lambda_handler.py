import logging
import os

import boto3

from common.constants import TAG_NAME, TAG_VALUE

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_client = None


def get_boto3_ec2_client():
    global _client
    if _client is not None:
        return _client

    aws_region = os.getenv('AWS_REGION')
    if aws_region:
        _client = boto3.client('ec2', region_name=aws_region)
    else:
        _client = boto3.client('ec2')
    return _client


def find_instances():
    client = get_boto3_ec2_client()

    filters = [
        {
            'Name': f'tag:{TAG_NAME}',
            'Values': [
                TAG_VALUE,
            ]
        },
        {
            'Name': 'instance-state-name',
            'Values': [
                'pending',
                'running',
            ]
        },
    ]

    response = client.describe_instances(Filters=filters)

    res_count = len(response['Reservations'])
    if res_count == 0:
        print('No instances found with provided search parameters')
        return []

    res = response['Reservations'][0]
    if 'Instances' not in res:
        print('No instances found with provided search parameters')
        return []

    instances = res['Instances']
    return instances


def lambda_handler(event, _):
    logger.info(event)

    instances = find_instances()
    if len(instances) > 0:
        return "Running instance(s): {}".format(
            ", ".join(list(map(lambda x: x['InstanceId'], instances)))
        )
    else:
        return "No instances running."
