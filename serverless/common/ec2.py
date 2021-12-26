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


def launch_instance(client, template_id):
    response = client.run_instances(
        MinCount=1,
        MaxCount=1,
        LaunchTemplate={
            'LaunchTemplateId': template_id,
        }
    )
    return response


def terminate_instances(client, instances):
    response = client.terminate_instances(
        InstanceIds=instances
    )
    return response


def find_launch_template(client, tag_name, tag_value) -> str:
    """
    Return the ID of the launch template with tag_name=tag_value
    """
    response = client.describe_launch_templates(
        Filters=[
            {
                'Name': f'tag:{tag_name}',
                'Values': [
                    tag_value,
                ]
            },
        ],
    )
    templates = response['LaunchTemplates']
    if len(templates) == 0:
        raise ValueError(f'No launch template found with tag {tag_name}={tag_value}')
    if len(templates) > 1:
        raise ValueError(f'Was expecting 1 template but found {len(template)}')
    return templates[0]['LaunchTemplateId']
