import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TAG_NAME = 'project'
TAG_VALUE = 'astropi'

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


def terminate_instances(instances):
    client = get_boto3_ec2_client()
    response = client.terminate_instances(
        InstanceIds=instances
    )
    return response


def lambda_handler(event, _):
    logger.info(event)

    instances = find_instances()
    if len(instances) == 0:
        msg = "No running instance(s) ==> Nothing to do"
        logger.info(msg)
        return msg

    instances = find_instances()
    instance_ids = list(map(lambda x: x['InstanceId'], instances))
    resp = terminate_instances(instance_ids)
    logger.debug(resp)

    msg = f"Terminated instances: {instance_ids}"
    logger.info(msg)

    return msg
