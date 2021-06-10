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


def find_launch_template() -> str:
    """
    Return the ID of the launch template with project=astropi
    """
    client = get_boto3_ec2_client()

    response = client.describe_launch_templates(
        Filters=[
            {
                'Name': f'tag:{TAG_NAME}',
                'Values': [
                    TAG_VALUE,
                ]
            },
        ],
    )
    templates = response['LaunchTemplates']
    if len(templates) == 0:
        raise ValueError('No launch template found with provided search paramters')
    if len(templates) > 1:
        raise ValueError(f'Was expecting 1 template but found {len(template)}')
    return templates[0]['LaunchTemplateId']


def run_instance(template_id):
    client = get_boto3_ec2_client()

    response = client.run_instances(
        MinCount=1,
        MaxCount=1,
        LaunchTemplate={
            'LaunchTemplateId': template_id,
        }
    )
    return response


def lambda_handler(event, _):
    logger.info(event)

    # pseudocode:
    # if an ec2 instance with tag project=astropi is already running, do nothing
    # if no ec2 instance with that tag is running, run one

    instances = find_instances()
    if len(instances) > 0:
        return "Running instance(s): {} ==> Not starting a new one.".format(
            list(map(lambda x: x['InstanceId'], instances)))

    launch_template_id = find_launch_template()
    resp = run_instance(launch_template_id)
    logger.info(resp)
    return "Launched instance"
