import os

import boto3

from common.constants import TAG_NAME, TAG_VALUE


def get_boto3_ec2_client():
    aws_region = os.getenv('AWS_REGION')
    if aws_region:
        client = boto3.client('ec2', region_name=aws_region)
    else:
        client = boto3.client('ec2')
    return client


def find_instances(client):
    """
    Find EC2 instances belonging to the project in pending or running state
    :param client: boto3 ec2 client
    :return: list of instance ids
    """
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